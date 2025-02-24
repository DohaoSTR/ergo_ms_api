"""
Файл для определения базовых классов предоставляющих механизм для выполнения команд через Poetry.
"""

import os

from typing import Optional

class PoetryCommand:
    """
        Базовый класс для выполнения команд через Poetry, включая Django команды и пользовательские Python скрипты.

        Этот класс предоставляет механизм для выполнения команд, как через `manage.py` (для Django), так и через
        обычные Python скрипты, которые могут быть указаны пользователем.

        Аргументы:
            poetry_command_name (str): Имя команды, которое будет использовано в Poetry.
            django_command_name (Optional[str]): Имя команды, которое будет передано Django через manage.py.
            script_command (Optional[str]): Имя пользовательской команды или Python скрипта, который будет выполнен.

        Методы:
            __init__(self, command_name: Optional[str] = None):
                Инициализация команды с указанием ее имени. Можно указать команду для Django или пользовательскую команду.
            
            run(self, *args):
                Выполняет команду с переданными аргументами. Формирует команду для выполнения и запускает ее.
        
        Пример:
            Для запуска в терминале команды, например `makemigrations`: 
            >>> poetry run cmd makemigrations

            Для использования Django команды, например `makemigrations`:
            >>> command = PoetryCommand(django_command_name="makemigrations")
            >>> command.run()

            Для выполнения пользовательского скрипта, например `my_script.py`: 
            >>> command = PoetryCommand(script_command="python my_script.py")
            >>> command.run()
    """
    poetry_command_name: str
    # Имя команды django
    django_command_name: Optional[str] = None
    # Пользовательская команда
    script_command: Optional[str] = None
    
    def __init__(self, command_name: Optional[str] = None):
        """
        Инициализация команды, которая будет выполнена.

        Принимает имя команды для выполнения, которое может быть:
        - командой Django (через `manage.py`), если указано поле `django_command_name`,
        - пользовательской командой или скриптом, если указано поле `script_command`.
        
        Если имя команды не указано, будет выбрано значение из одного из полей, если оно присутствует.
        
        Аргументы:
            command_name (Optional[str]): Имя команды для выполнения. Если не указано, используется значение из
                                          `django_command_name` или `script_command`.
        
        Исключения:
            ValueError: Если не указано имя команды для выполнения.
        """
        self.command_name = command_name or self.django_command_name or self.script_command

        if not self.command_name:
            raise ValueError("Не указано имя команды для выполнения.")

    def run(self, *args):
        """
        Выполняет команду с переданными аргументами.

        Формирует команду для выполнения, исходя из типа команды (Django или пользовательская команда),
        и запускает ее в операционной системе.

        Аргументы:
            *args (str): Аргументы, которые будут переданы в команду при выполнении. Они конкатенируются в строку.

        Исключения:
            RuntimeError: Если не удалось определить тип команды для выполнения (например, если не указаны
                          ни Django, ни пользовательские команды).
        
        Пример:
            Для команды `makemigrations` с дополнительными аргументами:
            >>> command = PoetryCommand(django_command_name="makemigrations")
            >>> command.run("--dry-run")

            Команда будет запущена как: `poetry run cmd makemigrations --dry-run`
            Команда будет выполнена как: `python src/manage.py makemigrations --dry-run`
        """
        args_str = " ".join(args)

        if self.django_command_name:
            command = f"python src/manage.py {self.command_name} {args_str}"
        elif self.script_command:
            command = f"{self.script_command} {args_str}"
        else:
            raise RuntimeError("Не удалось определить, какую команду выполнять.")

        os.system(command)

class FetchBitcoinPriceCommand(PoetryCommand):
    """
    Команда для получения текущей цены биткоина и сохранения её в БД.
    """
    poetry_command_name = "fetch_price"
    django_command_name = "fetch_price"

    def __init__(self):
        super().__init__(self.django_command_name)