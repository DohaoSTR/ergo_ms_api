"""
Файл содержащий API-представления (views) для Django-приложения.
"""

import os
import sys

import psycopg2

from rest_framework.response import Response
from rest_framework import status

from django.core.management import call_command
from django.db.utils import OperationalError
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from src.config.env import env
from src.config.settings.base import BASE_DIR
from src.core.utils.base.base_views import BaseAPIView

class CheckDatabaseConnectionView(BaseAPIView):
    """
    APIView для проверки подключения к базе данных и выполнения миграций.

    Методы:
        post(request, *args, **kwargs): Обрабатывает POST-запрос для проверки подключения к базе данных.
    """

    @swagger_auto_schema(
        operation_description="Проверка подключения к базе данных.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'host': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default='localhost',
                    description='Хост'
                ),
                'port': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default='5432',
                    description='Порт'
                ),
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default='postgres',
                    description='Имя пользователя'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_PASSWORD,
                    default='admin',
                    description='Пароль'
                ),
                'database': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default='ergo_ms',
                    description='База данных'
                ),
            },
            required=['host', 'port', 'username', 'password', 'database']
        ),
        responses={
            200: 'Подключение успешно.',
            400: 'Отсутствует один или несколько из требуемых параметров.',
            500: 'Нет подключения к базе данных.',
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос для проверки подключения к базе данных.

        Аргументы:
            request: Объект запроса, содержащий данные для подключения к базе данных.

        Возвращает:
            Response: Ответ с сообщением о результате подключения.
        """
        data = request.data

        host = data.get('host')
        port = data.get('port')
        username = data.get('username')
        password = data.get('password')
        database = data.get('database')

        # Проверка наличия всех необходимых параметров
        if not all([host, port, username, password, database]):
            return Response(
                {"message": "Отсутствует один или несколько из требуемых параметров: адрес сервера, username, password, or database"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Попытка подключения к базе данных
            connection = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                dbname=database
            )
            connection.close()

            # Обновляем .env файл с параметрами подключения
            env_file_path = os.path.join(BASE_DIR.parent.parent, '.env')
            
            # Сохраняем существующие переменные
            existing_vars = {}
            if os.path.exists(env_file_path):
                with open(env_file_path, 'r', encoding='utf-8') as env_file:
                    for line in env_file:
                        if '=' in line and not line.startswith(('DB_NAME=', 'DB_USER=', 'DB_PASSWORD=', 'DB_HOST=', 'DB_PORT=')):
                            key, value = line.strip().split('=', 1)
                            existing_vars[key] = value

            # Добавляем новые параметры БД
            env_content = ''
            for key, value in existing_vars.items():
                env_content += f"{key}={value}\n"
                
            # Добавляем параметры БД
            db_vars = {
                "DB_NAME": database,
                "DB_USER": username,
                "DB_PASSWORD": password,
                "DB_HOST": host,
                "DB_PORT": port,
            }
            for key, value in db_vars.items():
                env_content += f"{key}={value}\n"

            # Записываем обновленный файл
            with open(env_file_path, "w") as env_file:
                env_file.write(env_content)

            # Перезагружаем переменные окружения
            env.read_env(env_file_path)

            # Обновление настроек базы данных в Django
            settings.DATABASES['default'].update({
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': database,
                'USER': username,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,
            })

            # Выполнение миграций без вывода в консоль
            with open(os.devnull, 'w') as fnull:
                sys.stdout = fnull
                sys.stderr = fnull
                call_command('migrate')

            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            return Response({"message": "Подключение успешно."}, status=status.HTTP_200_OK)
        except (psycopg2.OperationalError, OperationalError) as e:
            error_message = (
                "Нет подключения к базе данных. "
                "Пожалуйста, проверьте, что сервер PostgreSQL запущен "
                "и доступен по указанным параметрам подключения."
            )
            return Response(
                {"message": error_message}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )