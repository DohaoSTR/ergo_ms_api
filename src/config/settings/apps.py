"""
Этот файл содержит настройки установленных приложений и middleware для Django-приложения.

Он использует функцию `discover_installed_apps` для автоматического обнаружения приложений в указанных директориях
и добавляет их в список установленных приложений. Также настраивает middleware, включая CORS middleware.

Middleware (промежуточное ПО) в контексте Django — это компонент, который обрабатывает запросы и ответы в 
процессе их прохождения через Django-приложение. Middleware позволяет выполнять различные задачи, такие 
как аутентификация, логирование, обработка ошибок, кэширование и многое другое, без необходимости изменять 
основной код приложения.
"""
from src.core.utils.auto_api.auto_config import discover_installed_apps

# Определяем директории для основных и внешних модулей
CORE_DIR = 'src/core'
EXTERNAL_MODULES_DIR = 'src/external'

# Обнаруживаем и устанавливаем основные и сторонние модули
CORE_APPS = discover_installed_apps(CORE_DIR)
EXTERNAL_MODULES_APPS = discover_installed_apps(EXTERNAL_MODULES_DIR)

DEVELOPED_APPS = CORE_APPS + EXTERNAL_MODULES_APPS

# Определяем список установленных приложений
INSTALLED_APPS = DEVELOPED_APPS + [
    'daphne',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_yasg',
]

# Определяем список middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]