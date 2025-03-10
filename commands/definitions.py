"""
Файл для определения Poetry команд.
"""

from commands.base import PoetryCommand

class MakeMigrationsCommand(PoetryCommand):
    """
    Команда для создания миграций Django.

    Используется для создания новых файлов миграций на основе изменений в моделях.
    """
    poetry_command_name = 'makemigrations'
    django_command_name = 'makemigrations'

    def __init__(self):
        super().__init__(self.django_command_name)

class MigrateCommand(PoetryCommand):
    """
    Команда для применения миграций Django.

    Применяет созданные миграции к базе данных.
    """
    poetry_command_name = 'migrate'
    django_command_name = 'migrate'

    def __init__(self):
        super().__init__(self.django_command_name)

class DevServerCommand(PoetryCommand):
    """
    Команда для запуска локального Django сервера в режиме разработки.

    Обычно используется для тестирования и отладки приложения.
    """
    poetry_command_name = 'dev'
    django_command_name = 'runserver'

    def __init__(self):
        super().__init__(self.django_command_name)

class ShellCommand(PoetryCommand):
    """
    Команда для запуска Django shell (интерактивной консоли).

    Позволяет работать с Python-кодом в контексте Django проекта.
    """
    poetry_command_name = 'shell'
    django_command_name = 'shell'

    def __init__(self):
        super().__init__(self.django_command_name)

class ProdServerCommand(PoetryCommand):
    """
    Команда для запуска production сервера (с использованием Daphne).

    Используется для запуска приложения в боевом режиме.
    """
    poetry_command_name = 'start_prod'
    django_command_name = 'start_prod'

    def __init__(self):
        super().__init__(self.django_command_name)

class StopProdServerCommand(PoetryCommand):
    """
    Команда для остановки продакшн сервера.

    Используется для завершения работы продакшн-сервера.
    """
    poetry_command_name = 'stop_prod'
    django_command_name = 'stop_prod'

    def __init__(self):
        super().__init__(self.django_command_name)

class ClearCacheCommand(PoetryCommand):
    """
    Команда для очистки кэша Django.

    Полезна для сброса устаревших данных из кэша.
    """
    poetry_command_name = 'clear_cache'
    django_command_name = 'clear_cache'

    def __init__(self):
        super().__init__(self.django_command_name)

class ClearPycacheCommand(PoetryCommand):
    """
    Команда для очистки pycache (кэшированных файлов Python).

    Обычно используется для удаления временных файлов .pyc.
    """
    poetry_command_name = 'clear_pycache'
    django_command_name = 'clear_pycache'

    def __init__(self):
        super().__init__(self.django_command_name)

class CollectStaticCommand(PoetryCommand):
    """
    Команда для сбора статических файлов в Django.

    Копирует статические файлы из приложений в единую директорию.
    """
    poetry_command_name = 'collectstatic'
    django_command_name = 'collectstatic'

    def __init__(self):
        super().__init__(self.django_command_name)

class AddModuleCommand(PoetryCommand):
    """
    Команда для добавления нового модуля в проект.

    Полезна для автоматизации процесса создания нового приложения или модуля.
    """
    poetry_command_name = 'add_module'
    django_command_name = 'add_module'

    def __init__(self):
        super().__init__(self.django_command_name)

class CreateSuperuserCommand(PoetryCommand):
    """
    Команда для создания суперпользователя Django.

    Позволяет создать нового суперпользователя с указанными именем и паролем.
    """
    poetry_command_name = 'createsuperuser'
    django_command_name = 'createsuperuser'

    def __init__(self):
        super().__init__(self.django_command_name)

class StartCeleryWorkerCommand(PoetryCommand):
    """
    Команда для запуска Celery.
    """
    poetry_command_name = 'start_celery_worker'
    django_command_name = 'start_celery_worker'

    def __init__(self):
        super().__init__(self.django_command_name)

class StopCeleryWorkerCommand(PoetryCommand):
    """
    Команда для остановки Celery worker.
    """
    poetry_command_name = 'stop_celery_worker'
    django_command_name = 'stop_celery_worker'


    def __init__(self):
        super().__init__(self.django_command_name)

class StartCeleryBeatCommand(PoetryCommand):
    """
    Команда для запуска Celery.
    """
    poetry_command_name = 'start_celery_beat'
    django_command_name = 'start_celery_beat'

    def __init__(self):
        super().__init__(self.django_command_name)

class StopCeleryBeatCommand(PoetryCommand):
    """
    Команда для остановки Celery beat.
    """
    poetry_command_name = 'stop_celery_beat'
    django_command_name = 'stop_celery_beat'

    def __init__(self):
        super().__init__(self.django_command_name)