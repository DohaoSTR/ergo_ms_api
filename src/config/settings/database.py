"""
Файл содержащий конфигурацию баз данных для Django-приложения.
Поддерживает множественные подключения к разным типам СУБД через YAML конфигурацию.
"""

from typing import Dict

import psycopg2
import yaml
import logging
import sqlite3
import os

import mysql.connector
import pyodbc

from django.core.exceptions import ImproperlyConfigured

import logging.config

from src.config.settings.logger import LOGGING
from src.config.settings.static import RESOURCES_DIR
from src.config.settings.base import SYSTEM_DIR

# Явная инициализация логирования
logging.config.dictConfig(LOGGING)

# Настройка логгера
logger = logging.getLogger('config.database')

# Маппинг поддерживаемых СУБД
DB_ENGINES = {
    'postgresql': 'django.db.backends.postgresql',
    'mysql': 'django.db.backends.mysql',
    'sqlite': 'django.db.backends.sqlite3',
    'mssql': 'django.db.backends.sqlserver',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

def get_database_configs() -> Dict:
    """
    Получает конфигурации баз данных из YAML файла
    """
    config_path = SYSTEM_DIR / 'databases.yaml'
    if not config_path.exists():
        error_msg = f"Файл конфигурации баз данных не найден: {config_path}"
        logger.error(error_msg)

        raise ImproperlyConfigured(error_msg)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        error_msg = f"Ошибка при чтении файла конфигурации: {str(e)}"
        logger.error(error_msg)
        raise ImproperlyConfigured(error_msg)
    
    if not config or 'databases' not in config:
        error_msg = "Неверный формат файла конфигурации баз данных"
        logger.error(error_msg)
        raise ImproperlyConfigured(error_msg)

    databases = {}
    for db_name, db_config in config['databases'].items():
        engine = db_config.get('engine', 'postgresql').lower()
        if engine not in DB_ENGINES:
            error_msg = (
                f"Неподдерживаемый тип СУБД: {engine}. "
                f"Поддерживаемые типы: {', '.join(DB_ENGINES.keys())}"
            )
            logger.error(error_msg)
            raise ImproperlyConfigured(error_msg)
        
        db_settings = {
            'ENGINE': DB_ENGINES[engine],
            'NAME': db_config['name'],
        }

        # SQLite требует только путь к файлу
        if engine != 'sqlite':
            db_settings.update({
                'USER': db_config['user'],
                'PASSWORD': db_config['password'],
                'HOST': db_config['host'],
                'PORT': db_config['port'],
            })

            # Настройки SSH туннеля
            if 'ssh' in db_config:
                logger.info(f"Настройка SSH туннеля для базы данных '{db_name}'")
                db_settings['SSH'] = {
                    'host': db_config['ssh'].get('host'),
                    'port': db_config['ssh'].get('port', 22),
                    'username': db_config['ssh'].get('username'),
                    'password': db_config['ssh'].get('password'),
                    'key_path': db_config['ssh'].get('key_path'),
                    'remote_host': db_config['host'],
                    'remote_port': db_config['port'],
                }

            # Специфичные настройки для разных СУБД
            if engine == 'mysql':
                db_settings.update({
                    'OPTIONS': {
                        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                        'charset': 'utf8mb4',
                    }
                })
            elif engine == 'mssql':
                db_settings.update({
                    'OPTIONS': {
                        'driver': 'ODBC Driver 17 for SQL Server',
                        'unicode_results': True,
                    },
                })

        databases[db_name] = db_settings
    
    return databases

# Получаем конфигурацию баз данных
try:
    DATABASES = get_database_configs()
except Exception as e:
    logger.error(f"Ошибка при загрузке конфигурации баз данных: {str(e)}")
    logger.warning("Используется пустая конфигурация базы данных")
    DATABASES = {
        'default': {}
    }

is_no_default_connection = True

# Проверяем подключение к каждой базе данных
for db_name, db_config in DATABASES.items():
    engine = db_config.get('ENGINE', '')
    
    if not db_config:
        logger.warning(f"Пропуск проверки подключения к '{db_name}': пустая конфигурация")
        continue

    try:
        if engine == DB_ENGINES['postgresql']:
            connection = psycopg2.connect(
                dbname=db_config['NAME'],
                user=db_config['USER'],
                password=db_config['PASSWORD'],
                host=db_config['HOST'],
                port=db_config['PORT']
            )
            connection.close()
        elif engine == DB_ENGINES['mysql']:
            connection = mysql.connector.connect(
                database=db_config['NAME'],
                user=db_config['USER'],
                password=db_config['PASSWORD'],
                host=db_config['HOST'],
                port=db_config['PORT']
            )
            connection.close()
        elif engine == DB_ENGINES['sqlite']:
            connection = sqlite3.connect(db_config['NAME'])
            connection.close()
        elif engine == DB_ENGINES['mssql']:
            connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={db_config['HOST']},{db_config['PORT']};"
                f"DATABASE={db_config['NAME']};"
                f"UID={db_config['USER']};"
                f"PWD={db_config['PASSWORD']}"
            )
            connection = pyodbc.connect(connection_string)
            connection.close()
        logger.info(f"Успешное тестовое подключение к базе данных '{db_name}' (тип: {engine})")
        if db_name == 'default':
            is_no_default_connection = False
    except Exception as e:
        error_msg = f"Не удалось подключиться к базе данных '{db_name}' (тип: {engine}): {str(e)}"
        logger.error(error_msg)

        if db_name == 'default':
            DATABASES[db_name] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(RESOURCES_DIR, 'db.sqlite3'),
            }
            logger.warning(f"База данных '{db_name}' переключена на SQLite для разработки")

        # Не прерываем работу сервера при ошибке подключения
        continue

if is_no_default_connection and 'default' not in DATABASES:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(RESOURCES_DIR, 'db.sqlite3'),
    }
    logger.warning("Создано подключение к SQLite по умолчанию, так как нет рабочего подключения default")