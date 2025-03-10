import json
import string

# SQL-запросы для получения информации о специальностях

def get_specialities(speciality_id: int = None):
    """
    Возвращает SQL-запрос и параметры для получения данных о конкретной специальности по её ID.

    Args:
        speciality_id (int, optional): ID специальности. Если не указан, возвращает запрос для всех специальностей.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и параметры для выполнения запроса.
               - SQL-запрос (str): Запрос для выборки данных о специальности.
               - Параметры (tuple): Кортеж с параметрами для запроса (speciality_id).
    """
    return (
        """
        select
            id,
            code,
            name,
            specialization,
            department,
            faculty,
            education_duration,
            year_of_admission
        from
            forecasting_module_speciality
        where id = %s
        """,
        (speciality_id,),  # Параметр для подстановки в SQL-запрос
    )

def get_all_specialities():
    """
    Возвращает SQL-запрос для получения данных обо всех специальностях.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и пустой кортеж параметров.
               - SQL-запрос (str): Запрос для выборки всех данных из таблицы специальностей.
               - Параметры (tuple): Пустой кортеж, так как параметры не требуются.
    """
    return (
        """
        select
            *
        from
            forecasting_module_speciality
        """,
        (),  # Пустой кортеж параметров, так как запрос не требует параметров
    )

# SQL-запросы для получения информации о дисциплинах

def get_disciplines(discipline_id: int = None):
    """
    Возвращает SQL-запрос и параметры для получения данных о конкретной дисциплине по её ID.

    Args:
        discipline_id (int, optional): ID дисциплины. Если не указан, возвращает запрос для всех специальностей.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и параметры для выполнения запроса.
                - SQL-запрос (str): Запрос для выборки данных о дисциплинах.
                - Параметра (tuple): Кортеж с параметрами для запроса (discipline_id).
    """
    return (
        """
        select
            id,
            code,
            name,
            semesters,
            contact_work_hours,
            independent_work_hours,
            controle_work_hours,
            competencies
        from
            forecasting_module_discpiline
        where id = %s
        """,
        (discipline_id,),  # Параметр для подстановки в SQL-запрос
    )

def get_all_disciplines():
    """
    Возвращает SQL-запрос для получения данных обо всех дисциплинах.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и пустой кортеж параметров.
               - SQL-запрос (str): Запрос для выборки всех данных из таблицы дисциплин.
               - Параметры (tuple): Пустой кортеж, так как параметры не требуются.
    
    """
    return (
        """
        select
            *
        from
            forecasting_module_discipline
        """,
        (),  # Пустой кортеж параметров, так как запрос не требует параметров
    )

# SQL-запросы для получения информации о матрице компетенций

def get_academicCompetenceMatrix(matrix_id: int = None):
    """
    Возвращает SQL-запрос и параметры для получения данных о матрице компетенций по её ID.

    Args:
        matrix_id (int, optional): ID матрицы. Если не указан, возвращает запрос для всех матриц академических компетенций.

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и параметры для выполнения запроса.
                - SQL-запрос (str): Запрос для выборки данных о матрицах компетенций.
                - Параметра (tuple): Кортеж с параметрами для запроса (matrix_id).
    """
    return (
        """
        select
            id,
            speciality_id,
            discipline_list,
            technology_stack
        from
            forecasting_module_academiccompetencematrix
        where id = %s
        """,
        (matrix_id,),  # Параметр для подстановки в SQL-запрос
    )

def get_allAcademicCompetenceMatrix():
    """
    Возвращает SQL-запрос для получения данных обо всех существующих матрицах компетенций

    Returns:
        tuple: Кортеж, содержащий SQL-запрос и пустой кортеж параметров.
               - SQL-запрос (str): Запрос для выборки всех данных из таблицы матриц академических компетенций.
               - Параметры (tuple): Пустой кортеж, так как параметры не требуются.
    """
    return (
        """
        select
            *
        from
            forecasting_module_academiccompetencematrix
        """,
        (),  # Пустой кортеж параметров, так как запрос не требует параметров
    )

    