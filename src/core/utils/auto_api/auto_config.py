"""
Файл с функциями для автоматизации сборки Django приложений (модулей).
"""

import os
import re
import importlib
import inspect
import logging

from typing import List

from django.apps import AppConfig
from django.urls import (
    include, 
    path
)

from src.config.env import env

logger = logging.getLogger('utils')

def discover_installed_apps(apps_dir: str) -> List[str]:
    """
    Рекурсивно обходит директории и находит установленные приложения.

    Аргументы:
        apps_dir (str): Базовая директория, в которой находятся приложения.

    Возвращает:
        list: Список строк, представляющих пути к установленным приложениям.
    """
    installed_apps = []

    def recursively_find_apps(current_dir: str, base_module: str) -> None:
        """
        Рекурсивно обходит директории и находит установленные приложения.

        Аргументы:
            current_dir (str): Текущая директория для обхода.
            base_module (str): Базовый модуль для текущей директории.
        """
        for app_name in os.listdir(current_dir):
            app_path = os.path.join(current_dir, app_name)
            if os.path.isdir(app_path):
                module_path = f'{base_module}.{app_name}'
                apps_py_path = os.path.join(app_path, 'apps.py')
                if os.path.exists(apps_py_path):
                    try:
                        app_module = importlib.import_module(f'src.{module_path}.apps')
                        app_config = None

                        for name, obj in inspect.getmembers(app_module, inspect.isclass):
                            if issubclass(obj, AppConfig) and obj is not AppConfig:
                                app_config = obj
                                break

                        if app_config:
                            installed_apps.append(f'src.{module_path}')
                    except ModuleNotFoundError:
                        logger.error("Модуль не найден: %s.apps", module_path)
                    except AttributeError:
                        logger.error("Ошибка атрибута: %s.apps не имеет допустимого класса AppConfig", module_path)
                else:
                    recursively_find_apps(app_path, module_path)

    recursively_find_apps(apps_dir, os.path.basename(apps_dir))

    return installed_apps

def discover_installed_app_urls(apps_dir: str, prefix: str) -> List[str]:
    """
    Рекурсивно обходит директории и находит URL-конфигурации для установленных приложений.

    Аргументы:
        base_path (str): Базовая директория, в которой находятся приложения.

    Возвращает:
        list: Список URL-конфигураций для установленных приложений.
    """
    urlpatterns = []
    # Получаем список всех подпапок в base_path
    for module_name in os.listdir(apps_dir):
        module_path = os.path.join(apps_dir, module_name)
        # Проверяем, является ли подпапка директорией
        if os.path.isdir(module_path):
            # Формируем путь для include
            if prefix == None:
                route = f"{prefix}/{module_name}/"
            else: 
                route = f"{module_name}/"

            url_pattern = path(route, include(f"src.{prefix}.{module_name}.urls"))
            urlpatterns.append(url_pattern)

    return urlpatterns

def check_app_config_name(directory: str, config_name: str) -> bool:
    """
    Проверяет все файлы apps.py в указанной директории на наличие определенного названия конфига.

    Аргументы:
        directory (str): Директория, в которой находятся файлы apps.py.
        config_name (str): Название конфига, которое нужно проверить.

    Возвращает:
        bool: True, если конфиг найден, иначе False.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'apps.py':
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as f:
                    content = f.read()

                    searched_class_signature = rf'class\s+{config_name}Config\s*\(AppConfig\):'
                    if re.search(searched_class_signature, content):
                        return True
    return False

def get_env_deploy_type():
    development = 'src.config.patterns.development'
    production = 'src.config.patterns.production'

    deploy_type = env.str('API_DEPLOY_TYPE', default='development')

    if deploy_type == 'production':
        return production
    else:
        return development