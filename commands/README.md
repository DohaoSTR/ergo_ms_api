# Скрипты Poetry для Django проекта

В этом документе описывается система команд Poetry, используемая для управления Django проектом. Скрипты предоставляют удобный интерфейс для выполнения различных команд Django и пользовательских скриптов.

## Структура директории

```
scripts/
├── __init__.py          # Инициализация пакета
├── __main__.py          # Точка входа для команд Poetry
├── base.py              # Базовые классы команд
└── definitions.py          # Определение конкретных команд
```

## Основные компоненты

### 1. Базовый класс команд (`base.py`)

`PoetryCommand` - базовый класс для всех команд, который обеспечивает:
- Выполнение Django команд через `src/manage.py`
- Обработку аргументов командной строки

### 2. Система команд (`definitions.py`)

Доступные команды:

| Команда Poetry | Django команда | Описание |
|---------------|----------------|-----------|
| makemigrations | makemigrations | Создание миграций базы данных |

| migrate | migrate | Применение миграций |
| dev | runserver | Запуск сервера разработки |
| prod | start_daphne | Запуск production сервера |
| stop_prod | stop_daphne | Остановка production сервера |
| shell | shell | Запуск Django shell |
| clear_cache | clear_cache | Очистка кэша |
| clear_pycache | clear_pycache | Очистка Python кэша |
| collectstatic | collectstatic | Сбор статических файлов |
| add_module | add_module | Добавление нового модуля |
| createsuperuser | createsuperuser | Создание суперпользователя |
| celery_worker | celery_worker | Запуск Celery worker |
| celery_beat | celery_beat | Запуск Celery beat |


## Использование

### Базовый синтаксис

```bash
poetry run cmd <команда> [аргументы...]
```

### Примеры использования

1. Запуск сервера разработки:
```bash
poetry run cmd dev
```

2. Создание миграций:
```bash
poetry run cmd makemigrations
```

3. Применение миграций:
```bash
poetry run cmd migrate
```

4. Сбор статических файлов:
```bash
poetry run cmd collectstatic --no-input
```

5. Запуск production сервера:
```bash
poetry run cmd prod
```

6. Создание модулей:
```bash
poetry run cmd add_module cms
poetry run cmd add_module cms adp
poetry run cmd add_module cms adp superuser
poetry run cmd add_module cms adp roles
```

### Интеграция с Poetry

Для работы скриптов необходимо добавить следующую секцию в `pyproject.toml`:

```toml
[tool.poetry.scripts]
cmd = "scripts.__main__:main"
```

## Расширение системы команд

Для добавления новой команды:

1. Создайте новый класс в `commands.py`, унаследованный от `PoetryCommand`
2. Определите атрибуты:
   - `poetry_command_name`: имя команды для вызова через Poetry
   - `django_command_name`: имя Django команды или
   - `script_command`: команда для выполнения пользовательского скрипта

Пример:
```python
class NewCommand(PoetryCommand):
    poetry_command_name = 'new_command'
    django_command_name = 'some_django_command'

    def __init__(self):
        super().__init__(self.django_command_name)
```

## Особенности реализации

1. **Динамическое обнаружение команд**
   - Все команды автоматически обнаруживаются при запуске
   - Новые команды добавляются автоматически при их определении в `commands.py`

2. **Обработка ошибок**
   - Проверка наличия команды перед выполнением
   - Вывод списка доступных команд при ошибке
   - Обработка отсутствующих аргументов

3. **Гибкость исполнения**
   - Поддержка как Django команд, так и пользовательских скриптов
   - Передача аргументов командной строки в команды

## Безопасность

- Команды выполняются в контексте Django проекта
- Проверка корректности команд перед выполнением
- Изоляция команд через Poetry окружение