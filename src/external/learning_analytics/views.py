from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.external.learning_analytics.models import (
    Technology,
    Competention
)
from src.external.learning_analytics.serializers import (
    TechnologySerializer,
    CompetentionSerializer
)
from src.core.utils.methods import parse_errors_to_dict
from src.core.utils.base.base_views import BaseAPIView
from src.external.learning_analytics.scripts import (
    get_technologies,
    get_all_technologies,
    get_competentions,
    get_all_competentions
)

from src.core.utils.database.main import OrderedDictQueryExecutor

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Представление данных для получения информации о компетенциях
class CompetentionGetView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Получение информации о компетенциях. Если указан параметр 'id', возвращается конкретная компетенция. Если параметр 'id' не указан, возвращаются все компетенции",
        manual_parameters=[
            openapi.Parameter(
                'id', # Имя параметра
                openapi.IN_QUERY, # Параметр передается в query-строке
                type = openapi.TYPE_INTEGER, # Тип параметра (целочисленный)
                required=False,
                description="Идентификатор компетенции (опционально)", # Описание параметра
            )
        ],
        responses={
            200: "Информация о компетенциях", # Успешный ответ
            400: "Ошибка" # Ошибка
        }
    )
    def get(self, request):
        """
        Обработка GET-запроса для получения информации о компетенциях.
        В случае передачи параметра 'id', возвращает данные о конкретной компетенциях.
        Если параметр 'id' не передан - возвращаются все данные о компетенциях.
        """
        competention_id = request.query_params.get('id') # Получаем параметр 'id' из query-строки

        if competention_id:
            # Если передан 'id', получаем данные о конкретной технологии
            competention = OrderedDictQueryExecutor.fetchall(
                get_competentions, competention_id = competention_id
            )
            if not competention:
                # Если компетенция не обнаружена - возвращаем ошибку 404
                return Response(
                    {"message": "Компетенция с указанным ID не найдена"},
                    status = status.HTTP_404_NOT_FOUND
                )
            # Формируем успешный ответ с данными о технологии
            response_data = {
                "data": competentions,
                "message": "Компетенция получена успешно"
            }
        else:
            # Если 'id' не передан, получаем данные обо всех технологиях
            competentions = OrderedDictQueryExecutor.fetchall(get_all_competentions)
            # Формируем успешный ответ с данными обо всех технологиях
            response_data = {
                "data": competentions,
                "message": "Все технологии получены успешно"
            }

        # Возвращаем ответ с данными и статусом 200
        return Response(response_data, status=status.HTTP_200_OK)

# Представление данных для получения информации о технологиях 
class TechnologyGetView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Получение информации о технологиях. Если указан параметр 'id', возвращается конкретная технология. Если параметр 'id' не указан, возвращаются все технологии.",
        manual_parameters=[
            openapi.Parameter(
                'id',  # Имя параметра
                openapi.IN_QUERY,  # Параметр передается в query-строке
                type=openapi.TYPE_INTEGER,  # Тип параметра (целочисленный)
                required=False,  # Параметр не обязательный
                description="Идентификатор технологии (опционально)",  # Описание параметра
            )
        ],
        responses={
            200: "Информация о технологиях",  # Успешный ответ
            400: "Ошибка"  # Ошибка
        }
    )
    def get(self, request):
        """
        Обрабатывает GET-запрос для получения информации о технологиях.
        Если передан параметр 'id', возвращает данные о конкретной технологии.
        Если параметр 'id' не передан, возвращает данные обо всех технологиях.
        """
        technology_id = request.query_params.get('id')  # Получаем параметр 'id' из query-строки

        if technology_id:
            # Если передан 'id', получаем данные о конкретной технологии
            technologies = OrderedDictQueryExecutor.fetchall(
                get_technologies, technology_id=technology_id
            )
            if not technologies:
                # Если технология не найдена, возвращаем ошибку 404
                return Response(
                    {"message": "Технология с указанным ID не найдена"},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Формируем успешный ответ с данными о технологии
            response_data = {
                "data": technologies,
                "message": "Технология получена успешно"
            }
        else:
            # Если 'id' не передан, получаем данные обо всех технологиях
            technologies = OrderedDictQueryExecutor.fetchall(get_all_technologies)
            # Формируем успешный ответ с данными обо всех технологиях
            response_data = {
                "data": technologies,
                "message": "Все технологии получены успешно"
            }

        # Возвращаем ответ с данными и статусом 200
        return Response(response_data, status=status.HTTP_200_OK)

# Представление данных для создания (POST) компетенций
class SendCompetentionView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Проверка ввода компетенции",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,  # Тип тела запроса (объект JSON)
            properties={
                'code': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (целое число)
                    description='Код'  # Описание поля
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Наименование'  # Описание поля
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Описание'  # Описание поля
                ),
            },
            required=['code', 'name', 'description'],  # Обязательные поля
            example={
                "code": "ОПК-8",
                "name": "Способен применять методы научных исследований при разработке информационно-аналитических систем безопасности",
                "description": "В этом случае компетенции соответствуют умения применять методы алгоритмизации, языки и технологии программирования при решении задач профессиональной деятельности, программировать, отлаживать и тестировать прототипы программно-технических комплексов, пригодные для практического применения"
            }
        ),
        responses={
            201: "Компетенция успешно сохранена",  # Успешный ответ
            400: "Произошла ошибка"  # Ошибка
        },
    )
    def post(self, request):
        """
        Обрабатывает POST-запрос для создания новой компетенции.
        Проверяет валидность данных и сохраняет компетенцию в базе данных.
        """
        serializer = CompetentionSerializer(data=request.data)  # Создаем сериализатор с данными из запроса

        if serializer.is_valid():
            # Если данные валидны, сохраняем технологию
            serializer.save()
            # Возвращаем успешный ответ
            successful_response = Response(
                {"message": "Компетенция сохранена успешно"},
                status=status.HTTP_200_OK
            )
            return successful_response

        # Если данные не валидны, преобразуем ошибки в словарь и возвращаем ошибку 400
        errors = parse_errors_to_dict(serializer.errors)
        return Response(
            errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# Представление данных для создания (POST) технологий
class SendTechnologyView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Проверка ввода технологии",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,  # Тип тела запроса (объект JSON)
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Название'  # Описание поля
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Описание'  # Описание поля
                ),
                'popularity': openapi.Schema(
                    type=openapi.TYPE_INTEGER,  # Тип поля (целое число)
                    description='Популярность'  # Описание поля
                ),
                'rating': openapi.Schema(
                    type=openapi.TYPE_INTEGER,  # Тип поля (целое число)
                    description='Рейтинг'  # Описание поля
                ),
            },
            required=['name', 'description', 'popularity', 'rating'],  # Обязательные поля
            example={
                "name": "Python",
                "description": "Python — это высокоуровневый язык программирования общего назначения, который широко используется для разработки веб-приложений, анализа данных, искусственного интеллекта и др.",
                "popularity": 95,
                "rating": 5
            }
        ),
        responses={
            201: "Технология успешно сохранена",  # Успешный ответ
            400: "Произошла ошибка"  # Ошибка
        },
    )
    def post(self, request):
        """
        Обрабатывает POST-запрос для создания новой технологии.
        Проверяет валидность данных и сохраняет технологию в базе данных.
        """
        serializer = TechnologySerializer(data=request.data)  # Создаем сериализатор с данными из запроса

        if serializer.is_valid():
            # Если данные валидны, сохраняем технологию
            serializer.save()
            # Возвращаем успешный ответ
            successful_response = Response(
                {"message": "Технология сохранена успешно"},
                status=status.HTTP_200_OK
            )
            return successful_response

        # Если данные не валидны, преобразуем ошибки в словарь и возвращаем ошибку 400
        errors = parse_errors_to_dict(serializer.errors)
        return Response(
            errors,
            status=status.HTTP_400_BAD_REQUEST
        )