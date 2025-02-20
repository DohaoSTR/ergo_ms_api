# Модули и подмодули

## Создание модуля
Новый модуль создается при помощи Poetry команды:
```bash
poetry run cmd add_module <имя_модуля>
```

Все модули создаются в папке `api/src/external`. Каждый модуль является отдельной папкой внутри `external`, например:
```
api/src/external/lms
api/src/external/bi
api/src/external/crm
```

## Создание подмодуля
Подмодуль создается при помощи Poetry команды:
```bash
poetry run cmd add_submodule <имя_модуля> <имя_подмодуля>
```

Подмодуль создается в папке модуля. Например, чтобы создать подмодуль `performance_evaluation` в модуле `lms`:
```
api/src/external/lms/performance_evaluation
```

# Структура модуля

Модуль является Django приложением и имеет следующую структуру:

```
module_name/
├── migrations/           # Папка с миграциями для БД
├── __init__.py          # Инициализация пакета и начальные настройки модуля
├── apps.py              # Конфигурация Django приложения
├── methods.py           # Вспомогательные методы модуля
├── models.py            # Модели данных (таблицы БД)
├── scripts.py           # Скрипты для интеграции и общей логики
├── serializers.py       # Django сериализаторы
├── tests.py             # Тесты модуля
├── urls.py              # URL маршруты API
└── views.py             # API представления (HTTP методы)
```

# Структура подмодуля

Подмодуль имеет схожую структуру, но без Django-специфичных файлов:

```
submodule_name/
├── __init__.py          # Инициализация пакета и начальные настройки подмодуля
├── methods.py           # Вспомогательные методы подмодуля
├── models.py            # Модели данных (таблицы БД)
├── scripts.py           # Скрипты для интеграции и общей логики
├── serializers.py       # Django сериализаторы
├── tests.py             # Тесты для подмодуля
├── urls.py              # URL маршруты API
└── views.py             # API представления (HTTP методы)
```

# Интеграция модулей

## Конфигурация интеграции
Интеграция между модулями настраивается в следующем файле:
```
api/src/config/modules_integration.conf
```

Пример конфигурации:
```conf
[ProcessGraphView]
path=processes/
method=GET
handler=src.handlers.statistic.tasks_graph_handler.handler
status_code=200
```

Где:
- `path` - URL-путь для интеграционного API-метода
- `method` - используемый HTTP-метод
- `handler` - путь к обработчику
- `status_code` - возвращаемый статус при успешном выполнении

## Обработчики интеграции
Обработчики создаются в папке `api/src/handlers` как функции `handler`. Каждый обработчик должен находиться в отдельном файле.

Пример обработчика для интеграции `lms` и `bi` модулей:

```python
from src.external.lms.scripts import get_tasks
from src.external.bi.scripts import transform_data_for_bi_graph

def handler():
    tasks = get_tasks(10, 10, 10)
    
    aggregation_params = [
        {
            "key": "status",
            "aggregation_type": "count",
            "data_source": "tasks"
        },
        {
            "key": "process_id",
            "aggregation_type": "unique_count",
            "data_source": "tasks"
        }
    ]
    
    graph_data = transform_data_for_bi_graph(tasks, aggregation_params)
    return {"data": graph_data}
```

# Автоматическая конфигурация

## Django приложения
Модули автоматически добавляются как Django приложения через функцию `discover_installed_apps` из `api/src/config/auto_config.py`. Эта функция сканирует `api/src/external` на наличие файлов `apps.py` и добавляет соответствующие приложения в `INSTALLED_APPS`.

## URL маршруты
URL-пути также добавляются автоматически функцией `discover_installed_app_urls` из `api/src/config/auto_config.py`. Функция находит все файлы `urls.py` в `api/src/external` и добавляет их маршруты в общую конфигурацию URL.

# Пример структуры LMS модуля

## Основной модуль: lms/
```
lms/
├── migrations/           # Папка с миграциями для БД
├── __init__.py          # Инициализация модуля
├── apps.py              # Конфигурация Django приложения
├── methods.py           # Общие методы LMS
├── models.py            # Базовые модели LMS
├── scripts.py           # Общие скрипты интеграции
├── serializers.py       # Общие сериализаторы
├── tests.py             # Тесты модуля
├── urls.py              # Основные URL маршруты
└── views.py             # Основные представления
```

## Подмодули:

### 1. students/ (Управление студентами)
```
lms/students/
├── __init__.py
├── methods.py           # Методы для работы со студентами
├── models.py           
    ├── Student         # Модель студента
├── scripts.py          # Скрипты для управления студентами
├── serializers.py      # Сериализаторы студенческих данных
├── tests.py           
├── urls.py            # URL для студенческих операций
└── views.py           # API для управления студентами
```

### 2. teachers/ (Управление преподавателями)
```
lms/teachers/
├── __init__.py
├── methods.py           # Методы для работы с преподавателями
├── models.py           
    ├── Teacher         # Модель преподавателя
    ├── Specialization  # Модель специализации преподавателя
    └── Schedule        # Модель расписания преподавателя
├── scripts.py          # Скрипты для управления преподавателями
├── serializers.py      # Сериализаторы данных преподавателей
├── tests.py           
├── urls.py            # URL для операций с преподавателями
└── views.py           # API для управления преподавателями
```

### 3. assignments/ (Управление заданиями)
```
lms/assignments/
├── __init__.py
├── methods.py         # Методы для работы с заданиями
├── models.py
    ├── Assignment    # Модель задания
    ├── Submission    # Модель ответа на задание
    └── Grade        # Модель оценки
├── scripts.py        # Скрипты для управления заданиями
├── serializers.py    # Сериализаторы заданий
├── tests.py
├── urls.py          # URL для операций с заданиями
└── views.py         # API для управления заданиями
```

### 4. progress/ (Отслеживание прогресса)
```
lms/progress/
├── __init__.py
├── methods.py        # Методы анализа прогресса
├── models.py
    ├── Progress     # Модель прогресса
    ├── Achievement  # Модель достижений
    └── Statistics   # Модель статистики
├── scripts.py       # Скрипты для анализа прогресса
├── serializers.py   # Сериализаторы прогресса
├── tests.py
├── urls.py         # URL для операций с прогрессом
└── views.py        # API для работы с прогрессом
```

### 5. communication/ (Коммуникации)
```
lms/communication/
├── __init__.py
├── methods.py       # Методы для коммуникаций
├── models.py
    ├── Message     # Модель сообщения
    ├── Chat        # Модель чата
    └── Notification # Модель уведомления
├── scripts.py      # Скрипты для управления коммуникациями
├── serializers.py  # Сериализаторы сообщений
├── tests.py
├── urls.py        # URL для коммуникаций
└── views.py       # API для коммуникаций
```

### 6. analytics/ (Аналитика)
```
lms/analytics/
├── __init__.py
├── methods.py      # Методы анализа данных
├── models.py
    ├── Report     # Модель отчета
    └── Metric     # Модель метрики
├── scripts.py     # Скрипты для генерации отчетов
├── serializers.py # Сериализаторы аналитических данных
├── tests.py
├── urls.py       # URL для аналитических операций
└── views.py      # API для аналитики
```

## Основные функции модулей:

1. **students**: Управление студентами.
2. **teachers**: Управление преподавателями.
3. **courses**: Создание и управление курсами, уроками, учебными материалами.
4. **assignments**: Создание заданий, прием работ, оценивание.
5. **progress**: Отслеживание успеваемости, достижения, статистика.
5. **communication**: Обмен сообщениями, уведомления, чаты.
6. **analytics**: Анализ данных, генерация отчетов, метрики обучения.

Каждый подмодуль следует принципу единой ответственности и содержит всю необходимую логику для работы со своей предметной областью. Взаимодействие между подмодулями осуществляется через четко определенные интерфейсы в методах и скриптах.
