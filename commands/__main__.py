"""
Файл для связи poetry и команд, созданных в commands.py.

Данный функционал взаимодействует с Poetry при помощи следующей секции pyproject.toml:

[tool.poetry.scripts]
cmd = "commands.__main__:main"

Пример команды для запуска сервера Django API:
>>> poetry run cmd dev
"""

import sys
import inspect
import logging
import threading
import time

from commands.definitions import PoetryCommand
from src.config.settings.logger import LOGGING

# Настройка логгера для скриптов
logger = logging.getLogger('commands')

# Использование форматтера из конфигурации
formatter = logging.Formatter(
    fmt=LOGGING['formatters']['simple']['format'],
    style=LOGGING['formatters']['simple']['style']
)

# Настройка вывода только в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


# def fetch_price_periodically(commands):
#     """
#     Фоновая задача для вызова fetch_price каждые 10 минут.
#     """
#     while True:
#         logger.info("Запуск команды fetch_price...")
#         CommandClass = commands.get("fetch_price")
#         if CommandClass:
#             try:
#                 CommandClass().run()
#                 logger.info("Команда fetch_price выполнена успешно.")
#             except Exception as e:
#                 logger.error(f"Ошибка при выполнении fetch_price: {e}")
#         else:
#             logger.error("Команда fetch_price не найдена.")
#         time.sleep(600)  # Запуск каждые 10 минут


def load_commands():
    """
    Загружает все доступные команды, которые являются подклассами PoetryCommand.
    """
    modules = sys.modules["commands.definitions"]
    commands = {
        cls.poetry_command_name: cls
        for _, cls in inspect.getmembers(modules, inspect.isclass)
        if issubclass(cls, PoetryCommand) and cls is not PoetryCommand
    }
    return commands


def main():
    """
    Точка входа для управления командами через Poetry.

    Пример использования:
        poetry run cmd <команда> [аргументы...]

        Например:
        poetry run cmd makemigrations --dry-run
        poetry run cmd dev
        poetry run cmd collectstatic --no-input
    """
    commands = load_commands()

    if len(sys.argv) < 2:
        logger.info("Использование: poetry run cmd <команда> [аргументы...]")
        logger.info("Доступные команды: %s", ", ".join(commands.keys()))
        return

    command_name = sys.argv[1]
    args = sys.argv[2:]

    CommandClass = commands.get(command_name)
    if not CommandClass:
        logger.error(f"Неизвестная команда: {command_name}")
        logger.info("Доступные команды: %s", ", ".join(commands.keys()))
        return

    # # Если запускается dev, то и запускается фоновый сбор цен
    # if command_name == "dev":
    #     logger.info("Запуск dev-сервера и фонового сбора цен на Bitcoin...")
    #     fetch_thread = threading.Thread(target=fetch_price_periodically, args=(commands,), daemon=True)
    #     fetch_thread.start()


    CommandClass().run(*args)


if __name__ == "__main__":
    main()
