"""
Файл конфигурации для автоматической генерации API эндпоинтов.

Этот файл содержит настройки для автоматической генерации API эндпоинтов на основе YAML конфигурации.
Он определяет доступные рендереры, пути к конфигурационным файлам и базовые настройки Swagger.

Основные компоненты:
- Настройки путей к конфигурационным файлам и обработчикам
- Список доступных рендереров для API ответов
- Базовые настройки Swagger документации

Использование:
    Конфигурация API эндпоинтов определяется в файле auto_api.yaml.
    Для каждого эндпоинта можно указать:
    - Путь и метод
    - Обработчик
    - Требуемые параметры
    - Настройки аутентификации
    - Ограничения частоты запросов
    - Документацию и примеры
"""

from rest_framework.renderers import (
    JSONRenderer,
    BrowsableAPIRenderer,
    StaticHTMLRenderer,
    TemplateHTMLRenderer
)

# Путь к файлу конфигурации API эндпоинтов
AUTO_API_CONFIG_PATH = 'src/config/auto_api'

# Базовый путь для поиска обработчиков API
STANDARD_HANDLERS_PATH = 'src.handlers.'

# Суффикс для методов-обработчиков
HANDLER_METHOD_NAME = '.handler'

# Словарь доступных рендереров для API ответов
AVAILABLE_RENDERERS = {
    'json': JSONRenderer,          # Рендерер JSON ответов
    'browsable': BrowsableAPIRenderer,    # Браузерный рендерер для тестирования API
    'html': StaticHTMLRenderer,    # Рендерер статического HTML
    'template': TemplateHTMLRenderer    # Рендерер HTML шаблонов
}

# Базовые настройки Swagger документации
AUTO_API_SWAGGER_SETTINGS = {
    'DEFAULT_TAG': 'Интеграция модулей',  # Тег по умолчанию для группировки эндпоинтов
    'DEFAULT_RENDERER': 'json',    # Рендерер по умолчанию
    'FILE_PARAM_NAME': 'file',     # Имя параметра для загрузки файлов
}