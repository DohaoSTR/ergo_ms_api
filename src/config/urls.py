"""
Файл для определения маршрутов URL для Django-API-приложения.

Он использует функцию `path` из `django.urls` для определения маршрутов и функцию `include`
для включения URL-конфигураций из других модулей. Также используется функция
`discover_installed_app_urls` для автоматического обнаружения и включения URL-конфигураций
из внешних модулей, находящихся в директории `EXTERNAL_MODULES_DIR`.
"""

from src.config.settings.auto_api import AUTO_API_CONFIG_PATH
from src.core.utils.auto_api.methods_generation import generate_routes_from_config

from src.core.utils.auto_api.auto_config import discover_installed_app_urls
from src.config.settings.apps import EXTERNAL_MODULES_DIR, CORE_DIR

urlpatterns = []

# Добавляем URL-конфигурации из ядра, автоматически 
# обнаруженные в директории CORE_DIR
core_modules_urlpatterns = discover_installed_app_urls(CORE_DIR, prefix='src.core')
urlpatterns += core_modules_urlpatterns

# Добавляем URL-конфигурации из внешних модулей, автоматически 
# обнаруженные в директории EXTERNAL_MODULES_DIR
external_modules_urlpatterns = discover_installed_app_urls(EXTERNAL_MODULES_DIR, prefix='src.external')
urlpatterns += external_modules_urlpatterns

# Добавляем URL-конфигурации из конфигурационного файла auto_api.yaml
config_urlpatterns = generate_routes_from_config(AUTO_API_CONFIG_PATH)
urlpatterns += config_urlpatterns
