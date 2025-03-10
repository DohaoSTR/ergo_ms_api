"""
Файл конфигурации Django приложения/модуля ADP.


Этот файл содержит класс конфигурации приложения, который определяет основные настройки,
такие как имя приложения и настройки базы данных по умолчанию.

Класс `AdpConfig`:
    Определяет конфигурацию приложения ADP, включая:
    - Тип поля первичного ключа по умолчанию
    - Имя приложения в системе
"""

from django.apps import AppConfig

class AdpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.core.cms.adp'