from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.core.utils.methods import parse_errors_to_dict
from src.core.utils.base.base_views import BaseAPIView
from src.core.utils.database.main import OrderedDictQueryExecutor
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from src.external.learning_analytics.forecasting_module.models import(
    Speciality,
    Discipline,
    AcademicCompetenceMatrix
)

from src.external.learning_analytics.forecasting_module.serializers import(
    SpecialitySerializer,
    DisciplineSerializer,
    AcademicCompetenceMatrixSerializer
)

from src.external.learning_analytics.forecasting_module.scripts import(
    get_specialities,
    get_all_specialities,
    get_disciplines,
    get_all_disciplines,
    get_academicCompetenceMatrix,
    get_allAcademicCompetenceMatrix
)

# Представление данных для получения информации о специальностях
class SpecialityGetView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Получение информации о направлениях подготовки. Если указан параметр 'id', возвращается конкретное направление. Если параметр 'id' не указан, возвращаются все направления",
        manual_parameters=[
            openapi.Parameter(
                'id', # Имя параметра
                openapi.IN_QUERY, # Параметр передается в query-строке
                type = openapi.TYPE_INTEGER, # Тип параметра (целочисленный)
                required=False,
                description="Идентификатор направления подготовки (опционально)", # Описание параметра
            )
        ],
        responses={
            200: "Информация о направлениях подготовки", # Успешный ответ
            400: "Ошибка" # Ошибка
        }
    )
    def get(self, request):
        """
        Обработка GET-запроса для получения информации о направлениях подготовки.
        В случае передачи параметра 'id', возвращает данные о направлениях подготовки.
        Если параметр 'id' не передан - возвращаются все данные о направлениях подготовки.
        """
        speciality_id = request.query_params.get('id') # Получаем параметр 'id' из query-строки

        if speciality_id:
            # Если передан 'id', получаем данные о конкретной специальности
            speciality = OrderedDictQueryExecutor.fetchall(
                get_specialities, speciality_id = speciality_id
            )
            if not speciality:
                # Если специальность не обнаружена - возвращаем ошибку 404
                return Response(
                    {"message": "Направление подготовки (специальность) с указанным ID не найдена"},
                    status = status.HTTP_404_NOT_FOUND
                )
            # Формируем успешный ответ с данными о специальности
            response_data = {
                "data": speciality,
                "message": "Специальность получена успешно"
            }
        else:
            # Если 'id' не передан, получаем данные обо всех специальностях
            specialities = OrderedDictQueryExecutor.fetchall(get_all_specialities)
            # Формируем успешный ответ с данными обо всех специальностях
            response_data = {
                "data": specialities,
                "message": "Все специальности получены успешно"
            }

        # Возвращаем ответ с данными и статусом 200
        return Response(response_data, status=status.HTTP_200_OK)

class SendSpecialityView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Проверка ввода специальности",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,  # Тип тела запроса (объект JSON)
            properties={
                'code': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Код специальности'  # Описание поля
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Наименование специальности'  # Описание поля
                ),
                'specialization': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Специализация'  # Описание поля
                ),
                'department': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Кафедра'  # Описание поля
                ),
                'faculty': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Факультет'  # Описание поля
                ),
                'education_duration': openapi.Schema(
                    type=openapi.TYPE_INTEGER,  # Тип поля (целое число)
                    description='Срок получения образования (в месяцах)'  # Описание поля
                ),
                'year_of_admission': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (целое число)
                    description='Год поступления'  # Описание поля
                ),
            },
            required=['code', 'name', 'specialization', 'department', 'faculty', 'education_duration', 'year_of_admission'],  # Обязательные поля
            example={
                "code": "10.05.04",
                "name": "Информационно-аналитические системы безопасности",
                "specialization": "Автоматизация информационно-аналитической деятельности",
                "department": "Компьютерные технологии и системы",
                "faculty": "Факультет информационных технологий",
                "education_duration": 66,  # 5 лет и 6 месяцев = 66 месяцев
                "year_of_admission": "2021"
            }
        ),
        responses={
            201: "Специальность успешно сохранена",  # Успешный ответ
            400: "Произошла ошибка"  # Ошибка
        },
    )
    def post(self, request):
        """
        Обрабатывает POST-запрос для создания новой специальности.
        Проверяет валидность данных и сохраняет специальность в базе данных.
        """
        serializer = SpecialitySerializer(data=request.data)  # Создаем сериализатор с данными из запроса

        if serializer.is_valid():
            # Если данные валидны, сохраняем специальность
            serializer.save()
            # Возвращаем успешный ответ
            successful_response = Response(
                {"message": "Специальность сохранена успешно"},
                status=status.HTTP_200_OK
            )
            return successful_response

        # Если данные не валидны, преобразуем ошибки в словарь и возвращаем ошибку 400
        errors = parse_errors_to_dict(serializer.errors)
        return Response(
            errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# Представление данных для получения информации о дисциплинах
class DisciplineGetView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Получение информации о дисциплинах. Если указан параметр 'id', возвращается конкретная дисциплина. Если параметр 'id' не указан, возвращаются все существующие дисциплины.",
        manual_parameters=[
            openapi.Parameter(
                'id', # Имя параметра
                openapi.IN_QUERY, # Параметр передается в query-строке
                type = openapi.TYPE_INTEGER, # Тип параметра (целочисленынй)
                required=False,
                description="Идентификатор дисциплины (опционально)", # Описание параметра
            )
        ],
        responses={
            200: "Информация о дисциплинах", # Успешный ответ
            400: "Ошибка" # Ошибка
        }
    )
    def get(self, request):
        """
        Обработка GET-запроса для получения информации о дисциплинах.
        В случае передачи параметра 'id', возвращает данные о дисциплинах.
        Если параметр 'id' не передан - возвращаются все данные о дисциплинах.
        """

        discipline_id = request.query_params.get('id') # Полчаем параметр 'id' из query-строки

        if discipline_id:
            # Если передан 'id', получаем данные о конкретной дисциплине
            discipline = OrderedDictQueryExecutor.fetchall(
                get_disciplines, discipline_id = discipline_id
            )
            if not discipline:
                # Если дисциплина не обнаружена - возвращаем ошибку 404
                return Response(
                    {"message": "Дисциплина с указанным ID не найдена"},
                    status = status.HTTP_404_NOT_FOUND
                )
            response_data = {
                "data": discipline,
                "message": "Дисциплина получена успешно."
            }
        else:
            # Если 'id' не передан, получаем данные обо всех специальностях
            disciplines = OrderedDictQueryExecutor.fetchall(get_all_disciplines)
            # Формируем успешный ответ с данными обо всех специальностях
            response_data = {
                "data": disciplines,
                "message": "Все дисциплины получены успешно"
            }

        # Возвращаем ответ с данными и статусом 200
        return Response(response_data, status=status.HTTP_200_OK)

class SendDisciplineView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Проверка ввода дисциплины",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, # Тип тела запроса (объект JSON)
            properties={
                'code': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Код специальности'  # Описание поля
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,  # Тип поля (строка)
                    description='Наименование специальности'  # Описание поля
                ),
                'semesters': openapi.Schema(
                    type=openapi.TYPE_STRING, # Тип поля (строка)
                    description='Период освоения дисциплины (номера семестров через запятую)' # Описание поля
                ),
                'contact_work_hours': openapi.Schema(
                    type=openapi.TYPE_INTEGER, # Тип поля (целочисленный)
                    description='Продолжительность контактной работы, ч' # Описание поля
                ),
                'independent_work_hours': openapi.Schema(
                    type=openapi.TYPE_INTEGER, # Тип поля (целочисленный)
                    description='Продолжительность самостоятельной работы, ч' # Описание поля
                ),
                'controle_work_hours': openapi.Schema(
                    type=openapi.TYPE_INTEGER, # Тип поля (целочисленный)
                    description='Продолжительность контроля, ч' # Описание поля
                ),
                'competencies': openapi.Schema(
                    type=openapi.TYPE_OBJECT, # Тип поля (объект)
                    description='Перечень приобретаемых компетенций' # Описание поля
                ),
            },
            required=['code', 'name', 'semesters', 'contact_work_hours', 'independent_work_hours', 'controle_work_hours'], # Обязательные поля
            example={
                'code': 'Б1.О.45',
                'name': 'Формализованные модели и методы решения аналитических задач',
                'semesters': '7,8',
                'contact_work_hours': 192,
                'independent_work_hours': 60,
                'controle_work_hours': 36,
                'competencies': {
                    'code': 'ОПК-1.2',
                    'name': '. Способен оценивать роль информации, информационных технологий и информационной безопасности в современном обществе.'
                }
            }
        ),
            responses={
                201: "Дисциплина успешно сохранена", # Успешный ответ
                400: "Произошла ошибка" # Ошибка
            },
        )
    def post(self, request):
            """
            Обрабатывает POST-запрос для создания новой дисциплины.
            Проверяет валидность данных и сохраняет дисциплину в базе данных.
            """

            serializer = DisciplineSerializer(data=request.data) # Создаем сериализатор с данными из запроса

            if serializer.is_valid():
                # Если данные валидны, сохраняем дисциплину
                serializer.save()
                # Возвращаем успешным ответ
                successful_response = Response(
                    {"message": "Специальность сохранена успешно"},
                    status= status.HTTP_200_OK
                )
                return successful_response
            
            # Если данные не валидны, преобразуем ошибки в словарь и возвращаем ошибку 400
            errors = parse_errors_to_dict(serializer.errors)
            return Response(
                errors,
                status=status.HTTP_400_BAD_REQUEST
            ) 


# Представление данных для получения информации об академических матрицах компетенций

class AcademicCompetenceMatrixGetView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Получение информации об академической матрице компетенций. Если указан параметр 'id', возвращается конкретная матрица. Если параметр 'id' не указан, возвращаются все существующие матрицы.",
        manual_parameters=[
            openapi.Parameter(
                'id', # Имя параметра
                openapi.IN_QUERY, # Параметр передается в query-строке
                type = openapi.TYPE_INTEGER, # Тип параметра (целочисленынй)
                required=False,
                description="Идентификатор академической матрицы компетенций (опционально)", # Описание параметра
            )
        ],
        responses={
            200: "Информация о матрицах академических компетенций", # Успешный ответ
            400: "Ошибка" # Ошибка
        }
    )
    def get(self, request):
        """
        Обработка GET-запроса для получения информации о матрицах академических компетенций.
        В случае передачи параметра 'id', возвращает данные о матрицах академических компетенций.
        Если параметр 'id' не передан - возвращаются все данные о матрицах академических компетенций.
        """

        matrix_id = request.query_params.get('id') # Полчаем параметр 'id' из query-строки

        if matrix_id:
            # Если передан 'id', получаем данные о конкретной дисциплине
            matrix = OrderedDictQueryExecutor.fetchall(
                get_academicCompetenceMatrix, matrix_id = matrix_id
            )
            if not matrix:
                # Если дисциплина не обнаружена - возвращаем ошибку 404
                return Response(
                    {"message": "Матрица академических компетенций с указанным ID не найдена"},
                    status = status.HTTP_404_NOT_FOUND
                )
            response_data = {
                "data": matrix,
                "message": "Матрица академических компетенций получена успешно."
            }
        else:
            # Если 'id' не передан, получаем данные обо всех специальностях
            matrices = OrderedDictQueryExecutor.fetchall(get_allAcademicCompetenceMatrix)
            # Формируем успешный ответ с данными обо всех специальностях
            response_data = {
                "data": matrices,
                "message": "Все матрицы академических компетенций получены успешно"
            }

        # Возвращаем ответ с данными и статусом 200
        return Response(response_data, status=status.HTTP_200_OK)

class SendAcademicCompetenceMatrixView(BaseAPIView):
    @swagger_auto_schema(
        operation_description="Проверка ввода матрицы академических компетенций",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, # Тип тела запроса (объект JSON)
            properties={
                'speciality_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,  # Тип поля (целочисленный)
                    description='Код специальности'  # Описание поля
                ),
                'discipline_list': openapi.Schema(
                    type=openapi.TYPE_OBJECT,  # Тип поля (объект)
                    description='Перечень изучаемых дисциплин'  # Описание поля
                ),
                'technology_stack': openapi.Schema(
                    type=openapi.TYPE_OBJECT, # Тип поля (строка)
                    description='Перечень изучаемых технологий в течение времени' # Описание поля
                ),                
            },
            required=['speciality_id', 'discipline_list', 'technology_stack'], # Обязательные поля
            example={
                'speciality_id': 1,
                'discipline_list': {
                    'code': 'Б1.О.45',
                    'name': 'Формализованные модели и методы решения аналитических задач',
                    'semesters': '7,8',
                    'contact_work_hours': 192,
                    'independent_work_hours': 60,
                    'controle_work_hours': 36,
                    'competencies': {
                        'code': 'ОПК-1.2',
                        'name': '. Способен оценивать роль информации, информационных технологий и информационной безопасности в современном обществе.'
                    }
                },
                'technology_stack': {
                    "name": "Python",
                    "description": "Python — это высокоуровневый язык программирования общего назначения, который широко используется для разработки веб-приложений, анализа данных, искусственного интеллекта и др.",
                    "popularity": 95,
                    "rating": 5
                }
            }
        ),
            responses={
                201: "Матрица академических компетенций успешно сохранена", # Успешный ответ
                400: "Произошла ошибка" # Ошибка
            },
        )
    def post(self, request):
            """
            Обрабатывает POST-запрос для создания новой матрицы академических компетенций.
            Проверяет валидность данных и сохраняет матрицы академических компетенций в базе данных.
            """

            serializer = AcademicCompetenceMatrixSerializer(data=request.data) # Создаем сериализатор с данными из запроса

            if serializer.is_valid():
                # Если данные валидны, сохраняем дисциплину
                serializer.save()
                # Возвращаем успешным ответ
                successful_response = Response(
                    {"message": "Матрица академических компетенций сохранена успешно"},
                    status= status.HTTP_200_OK
                )
                return successful_response
            
            # Если данные не валидны, преобразуем ошибки в словарь и возвращаем ошибку 400
            errors = parse_errors_to_dict(serializer.errors)
            return Response(
                errors,
                status=status.HTTP_400_BAD_REQUEST
            ) 
