import json
import string
import random
def get_technologies(technology_id: int = None):
    """
    Возвращает SQL-запрос и параметры для получения данных о технологиях.

    Args:
        technology_id (int, optional): ID технологии. Если не указан, возвращает запрос для всех технологий.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и параметры для выполнения запроса.
               - SQL-запрос (str): Запрос для выборки данных о технологиях.
               - Параметры (tuple): Кортеж с параметрами для запроса (technology_id, если указан).
    """
    if technology_id is not None:
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
    else:
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
    Возвращает SQL-запрос и параметры для получения данных о компетенциях.

    Args:
        competention_id (int, optional): ID компетенции. Если не указан, возвращает запрос для всех компетенций.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и параметры для выполнения запроса.
               - SQL-запрос (str): Запрос для выборки данных о компетенциях.
               - Параметры (tuple): Кортеж с параметрами для запроса (competention_id, если указан).
    """
    if competention_id is not None:
        return (
            """
            select
                id,
                code,
                name,
                description
            from
                learning_analytics_competention
            where id = %s
            """,
            (competention_id,),  # Параметр для подстановки в SQL-запрос
        )
    else:
        return (
            """
            select
                *
            from
                learning_analytics_competention
            """,
            (),  # Пустой кортеж параметров, так как запрос не требует параметров
        )

def get_employers(employer_id: int = None):
    """
    Возвращает SQL-запрос и параметры для получения данных о работодателях.

    Args:
        employer_id (int, optional): ID работодателя. Если не указан, возвращает запрос для всех существующих работодателей.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и параметры для выполнения запроса.
               - SQL-запрос (str): Запрос для выборки данных о работодателях.
               - Параметры (tuple): Кортеж с параметрами для запроса (employer_id, если указан).
    """
    if employer_id is not None:
        return (
            """
            select
                id,
                company_name,
                description,
                email,
                created_at,
                updated_at,
                rating
            from
                learning_analytics_employer
            where id = %s
            """,
            (employer_id,),  # Параметр для подстановки в SQL-запрос
        )
    else:
        return (
            """
            select
                *
            from
                learning_analytics_employer
            """,
            (),  # Пустой кортеж параметров, так как запрос не требует параметров
        )