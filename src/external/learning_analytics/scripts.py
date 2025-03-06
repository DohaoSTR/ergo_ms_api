import json
import string
import random

def get_technologies(technology_id: int = None):
    """
    Возвращает SQL-запрос и параметры для получения данных о конкретной технологии по её ID.

    Args:
        technology_id (int, optional): ID технологии. Если не указан, возвращает запрос для всех технологий.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и параметры для выполнения запроса.
               - SQL-запрос (str): Запрос для выборки данных о технологии.
               - Параметры (tuple): Кортеж с параметрами для запроса (technology_id).
    """
    return (
        """
        select
            id,
            name,
            description,
            popularity,
            rating
        from
            learning_analytics_technology
        where id = %s
        """,
        (technology_id,),  # Параметр для подстановки в SQL-запрос
    )


def get_all_technologies():
    """
    Возвращает SQL-запрос для получения данных обо всех технологиях.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и пустой кортеж параметров.
               - SQL-запрос (str): Запрос для выборки всех данных из таблицы технологий.
               - Параметры (tuple): Пустой кортеж, так как параметры не требуются.
    """
    return (
        """
        select
            *
        from
            learning_analytics_technology
        """,
        (),  # Пустой кортеж параметров, так как запрос не требует параметров
    )

def get_competentions(competention_id: int = None):
    """
    Возвращает SQL-запрос и параметры для получения данных о конкретной компетенции по её ID.

    Args:
        competention_id (int, optional): ID компетенции. Если не указан, возвращает запрос для всех существующих компетенций.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и параметры для выполнения запроса.
               - SQL-запрос (str): Запрос для выборки данных о компетенции.
               - Параметры (tuple): Кортеж с параметрами для запроса (competency_id).
    """
    return (
        """
        select
            id,
            code,
            name,
            description,
        from
            learning_analytics_competention
        where id = %s
        """,
        (competention_id,),  # Параметр для подстановки в SQL-запрос
    )

def get_all_competentions():
    """
    Возвращает SQL-запрос для получения данных обо всех компетенциях.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и пустой кортеж параметров.
               - SQL-запрос (str): Запрос для выборки всех данных из таблицы компетенций.
               - Параметры (tuple): Пустой кортеж, так как параметры не требуются.
    """
    return (
        """
        select
            *
        from
            learning_analytics_competention
        """,
        (),  # Пустой кортеж параметров, так как запрос не требует параметров
    )