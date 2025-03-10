"""
Файл для динамического создания API эндпоинтов на основе конфигурации.
"""

import importlib
import os
import yaml
import logging

from typing import Any, Dict, Tuple, Type, List

from django.urls import path
from django.http import FileResponse
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import NotFound, ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated

from src.core.utils.base.base_views import BaseAPIView

logger = logging.getLogger('utils')

# Настройки из конфига
class IntegrationSettings:
    """Класс для хранения настроек интеграции."""
    standard_handlers_path: str = getattr(settings, 'STANDARD_HANDLERS_PATH', '')
    handler_method_name: str = getattr(settings, 'HANDLER_METHOD_NAME', '')
    available_renderers: Dict = getattr(settings, 'AVAILABLE_RENDERERS', {})
    swagger_settings: Dict = getattr(settings, 'AUTO_API_SWAGGER_SETTINGS', {})

def load_handler(handler_path: str) -> Any:
    """
    Загрузка функции-обработчика из модуля.
    
    Args:
        handler_path: Путь к обработчику
        
    Returns:
        Загруженный обработчик
    """
    path = f"{IntegrationSettings.standard_handlers_path}{handler_path}{IntegrationSettings.handler_method_name}"
    module_name, func_name = path.rsplit('.', 1)
    
    try:
        module = importlib.import_module(module_name)
        return getattr(module, func_name)
    except (ImportError, AttributeError) as e:
        logger.error("Ошибка при загрузке обработчика %s: %s", handler_path, e)
        raise

def load_config(config_path: str) -> Dict:
    """
    Загрузка конфигурации из файла.
    
    Args:
        config_path: Путь к файлу конфигурации
        
    Returns:
        Загруженная конфигурация
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except (yaml.YAMLError, IOError) as e:
        logger.error("Ошибка при загрузке конфигурации: %s", e)
        raise

class SwaggerSchemaBuilder:
    """Класс для построения схемы Swagger."""
    
    type_mapping = {
        'string': openapi.TYPE_STRING,
        'integer': openapi.TYPE_INTEGER,
        'boolean': openapi.TYPE_BOOLEAN,
        'file': openapi.TYPE_FILE,
        'array': openapi.TYPE_ARRAY,
        'object': openapi.TYPE_OBJECT,
    }

    @staticmethod
    def get_param_info(param_value: Any) -> Dict[str, str]:
        """Получает информацию о параметре в унифицированном формате."""
        if isinstance(param_value, dict):
            return {
                'description': param_value.get('description', ''),
                'type': param_value.get('type', 'string')
            }
        return {'description': param_value, 'type': 'string'}

    @classmethod
    def create_file_parameter(cls) -> openapi.Parameter:
        """Создает параметр для загрузки файла."""
        return openapi.Parameter(
            name=IntegrationSettings.swagger_settings['FILE_PARAM_NAME'],
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description='Файл для загрузки'
        )

    @classmethod
    def create_parameters(cls, method: str, params_desc: Dict[str, Any],
                         required_params: List[str], optional_params: Dict[str, Any]) -> List[openapi.Parameter]:
        """Создает параметры для swagger документации."""
        if method in ["POST", "PUT", "PATCH"] and 'file' in required_params:
            return [cls.create_file_parameter()]

        if method in ["POST", "PUT", "PATCH"]:
            return cls.create_body_parameter(params_desc, required_params, optional_params)
        
        return cls.create_query_parameters(params_desc, required_params)

    @classmethod
    def create_body_parameter(cls, params_desc: Dict, required_params: List[str],
                            optional_params: Dict) -> List[openapi.Parameter]:
        """Создает параметры для тела запроса."""
        properties = {}
        required = []

        for param_name, param_value in params_desc.items():
            param_info = cls.get_param_info(param_value)
            if param_name in required_params:
                required.append(param_name)

            param_type = cls.type_mapping.get(param_info['type'], openapi.TYPE_STRING)
            properties[param_name] = openapi.Schema(
                type=param_type,
                description=param_info['description'],
                nullable=param_name in optional_params and optional_params[param_name] is None
            )

        schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties,
            required=required
        )

        return [openapi.Parameter(
            name='body',
            in_=openapi.IN_BODY,
            required=True,
            schema=schema
        )]

    @classmethod
    def create_query_parameters(cls, params_desc: Dict, required_params: List[str]) -> List[openapi.Parameter]:
        """Создает параметры для query-строки."""
        parameters = []
        for param_name, param_value in params_desc.items():
            param_info = cls.get_param_info(param_value)
            parameters.append(
                openapi.Parameter(
                    name=param_name,
                    in_=openapi.IN_QUERY,
                    description=param_info['description'],
                    required=param_name in required_params,
                    type=cls.type_mapping.get(param_info['type'], openapi.TYPE_STRING)
                )
            )
        return parameters

def create_handler_instance(handler_class, required_params, optional_params):
    """Создает экземпляр обработчика с параметрами из конфига."""
    return handler_class(required_params=required_params, optional_params=optional_params)

class BaseDynamicAPIView(BaseAPIView):
    """Базовый класс для динамических API views"""
    
    method = None
    handler = None
    status_code = None
    permission_classes = None
    
    def get_renderer_context(self):
        """Получение контекста для рендерера"""
        context = {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None)
        }
        return context
    
    def get_renderer(self):
        """Получение рендерера в зависимости от типа запроса"""
        # Для браузерных запросов возвращаем browsable рендерер
        if self.request and 'text/html' in self.request.META.get('HTTP_ACCEPT', ''):
            browsable_renderers = [r for r in self.renderer_classes if getattr(r, 'format', None) == 'api']
            if browsable_renderers:
                return browsable_renderers[0]()
        
        # Для остальных запросов используем JSON рендерер
        json_renderers = [r for r in self.renderer_classes if getattr(r, 'format', None) == 'json']
        if json_renderers:
            return json_renderers[0]()
        
        # Если ничего не подошло, используем первый доступный рендерер
        return self.renderer_classes[0]()
        
    def get_permissions(self):
        """Переопределяем метод для корректной работы permissions"""
        return [permission() for permission in self.permission_classes]
    
    def check_permissions(self, request):
        """Проверяем разрешения перед выполнением запроса"""
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def dispatch(self, request, *args, **kwargs):
        """Обработка входящего запроса"""
        self.args = args
        self.kwargs = kwargs
        self.headers = self.default_response_headers
        
        request = super().initialize_request(request, *args, **kwargs)
        self.request = request
        
        # Инициализируем throttle_info до блока try
        throttle_info = {}
        try:
            # Проверяем права доступа и throttling
            self.check_permissions(request)
            
            # Проверяем throttling и сохраняем информацию о нем
            for throttle in self.get_throttles():
                if not throttle.allow_request(request, self):
                    self.throttled(request, throttle.wait())
                # Сохраняем информацию о throttle после его инициализации
                if hasattr(throttle, 'get_rate'):
                    throttle_info[throttle.__class__.__name__] = {
                        'rate': throttle.get_rate(),
                        'num_requests': getattr(throttle, 'num_requests', None),
                        'duration': getattr(throttle, 'duration', None)
                    }
            
            if request.method == 'OPTIONS':
                response = self.options(request, *args, **kwargs)
            elif request.method != self.method:
                response = Response({"error": "Method not allowed"}, status=405)
            else:
                handler = self.get_handler()
                response = handler(request, *args, **kwargs)
                
        except PermissionDenied as e:
            response = Response(
                {"error": str(e) or "У вас нет прав для выполнения этого действия"}, 
                status=403
            )
        except Exception as exc:
            response = self.handle_exception(exc)

        if isinstance(response, Response):
            response.accepted_renderer = self.get_renderer()
            response.accepted_media_type = response.accepted_renderer.media_type
            response.renderer_context = self.get_renderer_context()

        return response

    def options(self, request, *args, **kwargs):
        """Обработка OPTIONS запроса"""
        metadata = {
            'name': self.__class__.__name__,
            'description': self.__doc__,
            'renders': [renderer.media_type for renderer in self.renderer_classes],
            'parses': ['application/json'],
            'allowed_methods': [self.method, 'OPTIONS']
        }
        
        response = Response(metadata)
        response.accepted_renderer = self.get_renderer()
        response.accepted_media_type = response.accepted_renderer.media_type
        response.renderer_context = self.get_renderer_context()
        
        return response

    def get_handler(self):
        """Получение обработчика для текущего метода"""
        if self.method.lower() == 'get':
            return self.get
        elif self.method.lower() == 'post':
            return self.post
        elif self.method.lower() == 'put':
            return self.put
        elif self.method.lower() == 'patch':
            return self.patch
        elif self.method.lower() == 'delete':
            return self.delete
        return None

def create_dynamic_api_view(method, renderers, handler, status_code, 
                            swagger_description, swagger_params, swagger_responses,
                            throttle_rates=None, tags=None):
    """Фабрика для создания классов DynamicAPIView"""
    class_name = f'DynamicAPIView_{method}'
    
    # Создаем динамические классы throttling если указаны специфические rates
    throttle_classes = []
    if throttle_rates:
        if 'anon' in throttle_rates:
            class CustomAnonRateThrottle(AnonRateThrottle):
                rate = throttle_rates['anon']
            throttle_classes.append(CustomAnonRateThrottle)
            
        if 'user' in throttle_rates:
            class CustomUserRateThrottle(UserRateThrottle):
                rate = throttle_rates['user']
            throttle_classes.append(CustomUserRateThrottle)

    # Преобразуем responses из конфига в формат для swagger
    swagger_response_schemas = {}
    for status_code_str, response_info in swagger_responses.items():
        try:
            response_status = int(status_code_str)
            
            # Создаем схему для ответа
            if isinstance(response_info, dict) and 'example' in response_info:
                example_data = response_info['example']
                
                if example_data == 'binary_data':
                    # Для бинарных данных
                    properties = {
                        'file': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format='binary'
                        )
                    }
                elif isinstance(example_data, dict):
                    # Для JSON ответов
                    properties = {}
                    for key, value in example_data.items():
                        if isinstance(value, dict):
                            nested_properties = {
                                k: openapi.Schema(
                                    type=openapi.TYPE_STRING if isinstance(v, str) 
                                    else openapi.TYPE_INTEGER if isinstance(v, int)
                                    else openapi.TYPE_OBJECT,
                                    example=v
                                ) for k, v in value.items()
                            }
                            properties[key] = openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties=nested_properties
                            )
                        else:
                            properties[key] = openapi.Schema(
                                type=openapi.TYPE_STRING if isinstance(value, str)
                                else openapi.TYPE_INTEGER if isinstance(value, int)
                                else openapi.TYPE_OBJECT,
                                example=value
                            )
                    
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties=properties
                )
                
                swagger_response_schemas[response_status] = openapi.Response(
                    description=response_info.get('description', ''),
                    schema=schema,
                    examples={'application/json': example_data} if example_data != 'binary_data' else None
                )
            else:
                # Для ответов без примеров
                swagger_response_schemas[response_status] = openapi.Response(
                    description=response_info.get('description', '')
                )
                
        except (ValueError, TypeError) as e:
            logger.error("Ошибка при обработке response для кода %s: %s", status_code_str, e)
            continue

    class_attrs = {
        'renderer_classes': renderers,
        'method': method.upper(),
        'handler': staticmethod(handler),
        'default_status_code': status_code,
        'throttle_classes': throttle_classes,
    }

    # Добавляем поддержку загрузки файлов для POST запросов
    if (method in ["POST", "PUT", "PATCH"] and 
        any(p.name == IntegrationSettings.swagger_settings['FILE_PARAM_NAME'] for p in swagger_params)):
        class_attrs['parser_classes'] = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description=swagger_description,
        manual_parameters=swagger_params,
        responses=swagger_response_schemas,  # Используем преобразованные схемы
        tags=tags,  # Используем извлеченные теги
    )
    def method_func(self, request, *args, **kwargs):
        try:
            # Проверяем аутентификацию перед выполнением запроса
            if not request.user.is_authenticated and self.permission_classes == [IsAuthenticated]:
                return Response(
                    {"detail": "Учетные данные не были предоставлены."}, 
                    status=401
                )
                
            if method in ["GET", "DELETE"]:
                query_params = request.query_params.dict()
                response = self.handler(**query_params, **kwargs)
                if isinstance(response, FileResponse):
                    return response
                data = response
            elif method in ["POST", "PUT", "PATCH"]:
                if request.FILES:
                    data = self.handler(
                        user=request.user,
                        **{IntegrationSettings.swagger_settings['FILE_PARAM_NAME']: 
                           request.FILES[IntegrationSettings.swagger_settings['FILE_PARAM_NAME']]}, 
                        **kwargs
                    )
                else:
                    body_data = request.data
                    data = self.handler(
                        user=request.user,
                        **body_data, 
                        **kwargs
                    )
            else:
                return Response({"error": "Неподдерживаемый метод"}, status=400)
            
            return Response(data, status=self.default_status_code)
            
        except NotFound as e:
            return Response({"error": str(e)}, status=404)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        except PermissionDenied as e:
            return Response({"error": "У вас нет прав для выполнения этого действия"}, status=403)
        except Exception as e:
            return Response(
                {"error": f"Внутренняя ошибка сервера: {str(e)}"}, 
                status=500
            )

    method_func.__name__ = method.lower()
    class_attrs[method.lower()] = method_func

    return type(class_name, (BaseDynamicAPIView,), class_attrs)

def create_api_view(name: str, config: dict) -> Tuple[str, Type[APIView]]:
    """Создает APIView на основе конфигурации."""
    endpoint_config = config[name]
    path = endpoint_config["path"]
    handler_path = endpoint_config["handler"]
    method = endpoint_config["method"]

    # Получаем настройки throttling из конфига
    throttle_rates = endpoint_config.get("throttle_rates", None)

    # Обязательные параметры
    status_code = endpoint_config.get("status_code", None)
    description = endpoint_config.get("description", "")
    # Получаем требование аутентификации из конфига
    auth_required = endpoint_config.get("auth_required", False)
    required_params = endpoint_config.get("required_params", [])
    optional_params = endpoint_config.get("optional_params", {})
    params_description = endpoint_config.get("params_description", {})
    responses = endpoint_config.get("responses", {})

    # Добавляем параметр tags в create_dynamic_api_view
    tags = endpoint_config.get("tags", [IntegrationSettings.swagger_settings['DEFAULT_TAG']]),
    
    # Добавляем стандартные ответы для случаев с требованием аутентификации
    if auth_required:
        responses.update({
            "401": {
                "description": "Не авторизован - Необходимо предоставить учетные данные",
                "example": {
                    "error": "Необходима аутентификация"
                }
            },
            "403": {
                "description": "Запрещено - У вас нет прав для доступа к этому ресурсу",
                "example": {
                    "error": "У вас нет прав для выполнения этого действия"
                }
            }
        })
    
    renderers_str = endpoint_config.get("renderers", IntegrationSettings.swagger_settings['DEFAULT_RENDERER']).lower()
    renderer_names = [r.strip() for r in renderers_str.split(',')]
    renderers = [IntegrationSettings.available_renderers[r] for r in renderer_names if r in IntegrationSettings.available_renderers]
    
    if not renderers:
        renderers = [IntegrationSettings.available_renderers[IntegrationSettings.swagger_settings['DEFAULT_RENDERER']]]

    module_name = IntegrationSettings.standard_handlers_path + handler_path
    module = importlib.import_module(module_name)
    handler_class = getattr(module, 'HandlerClass')
    
    handler = create_handler_instance(handler_class, required_params, optional_params)

    swagger_params = SwaggerSchemaBuilder.create_parameters(
        method, params_description, required_params, optional_params
    )

    DynamicAPIView = create_dynamic_api_view(
        method=method,
        renderers=renderers,
        handler=handler,
        status_code=status_code,
        swagger_description=description,
        swagger_params=swagger_params,
        swagger_responses=responses,
        throttle_rates=throttle_rates,
        tags=tags,
    )

    # Создаем новый класс с нужными permission_classes
    class CustomDynamicAPIView(DynamicAPIView):
        permission_classes = [IsAuthenticated] if auth_required else [permissions.AllowAny]

    CustomDynamicAPIView.__name__ = name

    #reconstructed_code = reconstruct_class_code(CustomDynamicAPIView)
    
    return path, CustomDynamicAPIView

def generate_routes_from_config(configs_path: List[str]) -> list:
    """Генерирует маршруты из конфигурации."""
    # Перебираем все файлы в указанной директории
    for filename in os.listdir(configs_path):
        # Проверяем, является ли файл YAML файлом
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            config_path = os.path.join(configs_path, filename)

            config = load_config(config_path)
            routes = []

            for section_name in config:
                path_s, view = create_api_view(section_name, config)
                routes.append(path(path_s, view.as_view()))

            return routes
        
    return []