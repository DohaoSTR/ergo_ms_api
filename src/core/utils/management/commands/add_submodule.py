import os
import logging

from typing import Any, Dict
from textwrap import dedent

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from src.core.utils.auto_api.auto_config import check_app_config_name
from src.core.utils.methods import convert_snake_to_camel

# Настройка логгера
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Команда Django для создания нового подмодуля внутри существующего модуля.
    Attributes:
        help (str): Описание команды для справки Django.
    """
    help = 'Создание нового подмодуля внутри существующего модуля в директории src/external'

    def add_arguments(self, parser) -> None:
        """
        Добавляет аргументы командной строки для команды.
        Args:
            parser: Парсер аргументов Django.
        """
        parser.add_argument('module_name', help='Имя существующего модуля')
        parser.add_argument('submodule_name', help='Имя создаваемого подмодуля')

    def create_file_structure(self, module_directory: str, files_to_create: Dict[str, str]) -> None:
        """
        Создает файловую структуру модуля.

        Args:
            module_directory (str): Путь к директории модуля
            files_to_create (Dict[str, str]): Словарь с именами файлов и их содержимым
        """
        for filename, content in files_to_create.items():
            file_path = os.path.join(module_directory, filename)
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content.strip())
                logger.debug(f'Создан файл: {file_path}')
            except IOError as e:
                logger.error(f'Ошибка при создании файла {file_path}: {str(e)}')
                raise CommandError(f'Не удалось создать файл {filename}')

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Выполняет команду создания подмодуля.
        Args:
            *args: Позиционные аргументы
            **options: Именованные аргументы, включая module_name и submodule_name
        Raises:
            CommandError: Если модуль или подмодуль уже существует или возникла ошибка при создании
        """
        module_name = options['module_name']
        submodule_name = options['submodule_name']

        logger.info(f'Начало создания подмодуля {submodule_name} внутри модуля {module_name}')

        external_modules_directory = getattr(settings, 'EXTERNAL_MODULES_DIR', None)
        if not external_modules_directory:
            logger.error('Директория EXTERNAL_MODULES_DIR не настроена в settings.')
            self.stdout.write(self.style.ERROR('Директория EXTERNAL_MODULES_DIR не настроена в settings.'))
            return

        # Проверяем, существует ли основной модуль
        module_directory = os.path.normpath(os.path.join(external_modules_directory, module_name))
        if not os.path.exists(module_directory):
            logger.error(f'Модуль {module_name} не существует: {module_directory}')
            self.stdout.write(self.style.ERROR(f'Модуль {module_name} не существует по пути - {module_directory}.'))
            return

        # Создаем директорию для подмодуля
        submodule_directory = os.path.normpath(os.path.join(module_directory, submodule_name))
        if os.path.exists(submodule_directory):
            logger.error(f'Подмодуль {submodule_name} уже существует: {submodule_directory}')
            self.stdout.write(self.style.ERROR(f'Подмодуль {submodule_name} уже существует по пути - {submodule_directory}.'))
            return
        
        camel_submodule_name = convert_snake_to_camel(submodule_name)
        if check_app_config_name(external_modules_directory, camel_submodule_name):
            logger.error(f'Конфликт имен: {camel_submodule_name}Config уже существует')
            self.stdout.write(self.style.ERROR(f'Уже существует модуль c именем класса конфига - {camel_submodule_name}Config.'))
            self.stdout.write(self.style.ERROR(f'Попробуйте другое название модуля.'))
            return

        try:
            os.makedirs(submodule_directory) 
            os.makedirs(os.path.join(submodule_directory, 'migrations'))
            logger.debug(f'Создана директория для подмодуля {submodule_name}')

            # Файлы для подмодуля
            files_to_create = {
                '__init__.py': '',
                'apps.py': dedent(f"""
                    from django.apps import AppConfig

                    class {camel_submodule_name}Config(AppConfig):
                        default_auto_field = 'django.db.models.BigAutoField'
                        name = 'src.external.{module_name}.{submodule_name}'
                """),
                'urls.py': dedent("""
                    from django.urls import path

                    urlpatterns = [
                    ]
                """),
                'models.py': dedent("""
                    from django.db import models

                    # Создавайте свои модели здесь
                """),
                'scripts.py': dedent("""
                    # Создавайте свои скрипты здесь
                """),
                'tests.py': dedent("""
                    from django.test import TestCase

                    # Создавайте свои тесты здесь
                """),
                'serializers.py': dedent("""
                    from rest_framework import serializers

                    # Создавайте свои сериализаторы здесь
                """),
                'methods.py': dedent("""
                    # Создавайте свои вспомогательные методы здесь
                """),
                'views.py': dedent("""
                    from django.shortcuts import render

                    # Создавайте свои представления здесь
                """),
                os.path.join('migrations', '__init__.py'): '',
            }

            self.create_file_structure(submodule_directory, files_to_create)

            logger.info(f'Подмодуль {submodule_name} успешно создан внутри модуля {module_name}')
            self.stdout.write(
                self.style.SUCCESS(f'Подмодуль {submodule_name} успешно создан по пути - {submodule_directory}')
            )

        except Exception as e:
            logger.error(f'Ошибка при создании подмодуля: {str(e)}')
            raise CommandError(f'Не удалось создать подмодуль: {str(e)}')