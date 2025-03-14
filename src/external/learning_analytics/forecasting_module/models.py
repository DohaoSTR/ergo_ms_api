from django.db import models
from src.external.learning_analytics.models import (
    Employer
)

class Speciality(models.Model):
    """
    Модель Speciality представляет собой информацию о специальности (направлении подготовки).

    Attributes:
        code (CharField): Код специальности. Максимальная длина — 20 символов.
        name (CharField): Наименование специальности. Максимальная длина — 255 символов.
        specialization (CharField): Наименование специализации. Максимальная длина - 255 символов.
        department (CharField): Кафедра, выпускающая специальность. Максимальная длина - 255 символов.
        faculty (CharField): Факультет. Максимальная длина - 255 символов.
        education_duration (SmallAutoField): Срок получения образования. Подразумевается измерение в количестве месяцев. 
        year_of_admission (CharField): Год поступления (для учета различий в УП)
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код специальности")
    name = models.CharField(max_length=255, verbose_name="Специальность")
    specialization = models.CharField(max_length=255, verbose_name="Специализация")
    department = models.CharField(max_length=255, verbose_name="Кафедра")
    faculty = models.CharField(max_length=255, verbose_name="Факультет")
    education_duration = models.PositiveSmallIntegerField(verbose_name="Срок получения образования")
    year_of_admission = models.CharField(max_length=4, verbose_name="Год поступления")

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"


class Discipline(models.Model):
    """
    Модель Discipline представляет собой информацию о дисциплине.
    
    Attributes:
        code (CharField): Код дисциплины. Максимальна длина - 10 символов.
        name (CharField): Наименование дисциплины. Максимальная длина - 255 символов.
        semesters (CharField): Период освоения дисциплины (номера семестров через ','). Максимальная длина - 12 символов.
        contact_work_hours (SmallAutoField): Длительность контактной работы, часы. 
        independent_work_hours (SmallAutoField): Длительность самостоятельной работы, часы.
        controle_work_hours (SmallAutoField): Длительность контроля, часы
        competencies (JSONField): Перечень осваиваемых компетенций
    """
    code = models.CharField(max_length=10, unique=True, verbose_name="Код дисциплины")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    # Подразумевается максимум 6 семестров
    semesters = models.CharField(max_length=12, verbose_name="Период освоения (семестры)")
    contact_work_hours = models.PositiveSmallIntegerField(verbose_name="Контактная работа, ч")
    independent_work_hours = models.PositiveSmallIntegerField(verbose_name="Самостоятельная работа, ч")
    controle_work_hours = models.PositiveSmallIntegerField(verbose_name="Контроль, ч")
    # todo: Подразумевается дополнительно включить логику рассмотрения рабочих планов по дисциплине (РПД хранят расписанные перечни компетенций)
    competencies = models.JSONField(verbose_name="Осваиваемые компетенции")

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

class AcademicCompetenceMatrix(models.Model):
    """
    Модель AcademicCompetenceMatrix - модель, представляющая матрицу академических компетенций, на основании
    которой в дальнейшем будет формироваться основной вектор индивидуальной траектории обучения.


    Attributes:

        speciality (ForeignKey): Внешний ключ, связывающий матрицу с моделью специальности
        discipline_list  (JSONField): Перечень осваиваемых дисциплин (хранит указатели на дисциплины)
        technology_stack  (JSONField): Изучаемый стек технологий (подразумевается дублирование для дальнейшего приоритета и распределения)
    """


    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.SET_NULL,
        verbose_name="Специальность",
        blank = True,
        null = True)  
    discipline_list = models.JSONField(verbose_name="Перечень изучаемых дисциплин")
    technology_stack  = models.JSONField(verbose_name="Перечень изучаемых технологий в течение времени")

    def __str__(self):
        return f"Матрица академических компетенций для {self.speciality}"

    class Meta:
        verbose_name = "Матрица академических компетенций"
        verbose_name_plural = "Матрицы академических компетенций"

class CompetencyProfileOfVacancy(models.Model):
    """
    Модель CompetencyProfileOfVacancy - модель, представляющая компетентностный профиль вакансии, на основании
    которой в дальнейшем будет формироваться дополнительный вектор индивидуальных траекторий обучения, соотевтствующий
    запросам работодателей.

    Attributes:
        vacancy_name (CharField): Название вакансии, отражающее содержание компетентностного профиля
        employer  (PositiveSmallIntegerField): ID работодателя, сформировавшего вакансию
        competencies_stack  (JSONField): Перечень запрашиваемых компетенций работодателем
        technology_stack (JSONField): Перечень технологий, запрашиваемых работодателем
        descr (TextField): Описание вакансии (исходное)
    """

    vacancy_name = models.CharField(max_length=255, verbose_name="Название вакансии")
    employer = models.ForeignKey(
        Employer, 
        on_delete=models.SET_NULL,
        verbose_name="ID работодателя",
        blank = True,
        null = True)
    competencies_stack = models.JSONField(verbose_name="Перечень требующихся компетенций")
    technology_stack = models.JSONField(verbose_name="Стек требуемых технологий")
    descr = models.TextField(max_length=400, verbose_name="Описание вакансии")

    def __str__(self):
        return f"Компетентностный профиль вакансии {self.vacancy_name}"
    
    class Meta:
        verbose_name = "Компетентностный профиль вакансии"
        verbose_name_plural = "Компетентностные профили вакансии"
