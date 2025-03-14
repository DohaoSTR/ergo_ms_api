# Импорт необходимых классов и модулей из Django REST Framework
from rest_framework.serializers import (
    ModelSerializer,            # Базовый класс для создания сериализаторов на основе моделей
    CharField,                  # Поле для строковых данных
    BooleanField,               # Поле для булевых значений
    ValidationError,            # Класс для обработки ошибок валидации
    Serializer                  # Базовый класс для создания кастомных сериализаторов
)

# Импорт модели Technology из приложения learning_analytics
from src.external.learning_analytics.forecasting_module.models import (
    Speciality,                 # Модель специальностией
    Discipline,                 # Модель дисциплины
    AcademicCompetenceMatrix,   # Модель матрицы академических компетенций
    CompetencyProfileOfVacancy  # Модель компетентностного профиля вакансии
)

# Создание сериализатора для модели Speciality
class SpecialitySerializer(ModelSerializer):
    class Meta:
        # Указываем модель, с которой работает сериализатор
        model = Speciality
        # Указываем поля модели, которые будут сериализованы/десериализованы
        fields = ['code', 'name', 'specialization', 'department', 'faculty', 'education_duration', 'year_of_admission']

        # Метод для создания нового объекта Speciality
        def create(self, validated_data):
            """
            Создаёт новый объект Speciality на основе валидированных данных

            :param validated_data: Данные, прошедшие валидацию
            :return: Созданный объект Speciality
            """
            speciality = Speciality.objects.create(
                code=validated_data['code'],                             # Устанавливаем код специальности
                name=validated_data['name'],                             # Устанавливаем наименование специальности
                specialization=validated_data['specialization'],         # Устанавливаем специализацию специальности
                department=validated_data['department'],                 # Устанавливаем кафедру специальности
                faculty=validated_data['faculty'],                       # Устанавливаем факультет специальности
                education_duration=validated_data['education_duration'], # Устанавливаем продолжительность обучения по специальности
                year_of_admission=validated_data['year_of_admission'],   # Устанавливаем год поступления на специальность
            )

            return speciality # Возвращаем созданный объект


# Создание сериализатора для модели Discipline
class DisciplineSerializer(ModelSerializer):
    class Meta:
        # Указываем модель, с которой работает сериализатор
        model = Discipline
        # Указываем поля модели, которые будут сериализованы/десериализованы
        fields = ['code', 'name', 'semesters', 'contact_work_hours', 'independent_work_hours', 'controle_work_hours', 'competencies']

        # Метод для создания нового объекта Speciality
        def create(self, validated_data):
            """
            Создаёт новый объект Discipline на основе валидированных данных

            :param validated_data: Данные, прошедшие валидацию
            :return: Созданный объект Discipline
            """
            discipline = Discipline.objects.create(
                code=validated_data['code'],                                        # Устанавливаем код дисциплины
                name=validated_data['name'],                                        # Устанавливаем наименование дисциплины
                semesters=validated_data['semesters'],                              # Устанавливаем период освоения дисциплины
                contact_work_hours=validated_data['contact_work_hours'],            # Устанавливаем продолжительность контактной работы
                independent_work_hours=validated_data['independent_work_hours'],    # Устанавливаем продолжительность самостоятельной работы
                controle_work_hours=validated_data['controle_work_hours'],          # Устанавливаем продолжительность контроля
                competencies=validated_data['competencies'],                        # Устанавливаем перечень осваиваемых компетенций
            )

            return discipline # Возвращаем созданный объект

class AcademicCompetenceMatrixSerializer(ModelSerializer):
    class Meta:
        # Указываем модель, с которой работает сериализатор
        model = AcademicCompetenceMatrix
        # Указываем поля модели, которые будут сериализованы/десериализованы
        fields = ['speciality_id', 'discipline_list', 'technology_stack']

        # Метод для создания нового объекта Speciality
        def create(self, validated_data):
            """
            Создаёт новый объект Discipline на основе валидированных данных

            :param validated_data: Данные, прошедшие валидацию
            :return: Созданный объект Discipline
            """

            AcademicCompetenceMatrix = AcademicCompetenceMatrix.objects.create(
                speciality_id=validated_data['speciality_id'],                      # Устанавливаем id специальности, для которой формируется матрица академических компетенций
                discipline_list=validated_data['discipline_list'],                  # Устанавливаем перечень осваиваемых дисциплин
                technology_stack=validated_data['technology_stack'],                # Устанавливаем перечень приобретаемых технологий
            )

            return AcademicCompetenceMatrix # Возвращаем созданный объект

class CompetencyProfileOfVacancySerializer(ModelSerializer):
    class Meta:
        # Указываем модель, с которой будет работать сериализатор
        model = CompetencyProfileOfVacancy
        # Указываем поля модели, которые будут серилаизованы/десериализованы
        fields = ['vacancy_name', 'employer_id', 'competencies_stack', 'technology_stack', 'descr']

        # Метод для создания нового объекта CompetencyProfileOfVacancy
        def create(self, validated_data):
            """
            Создает новый объект CompetencyProfileOfVacancy на основе валидированных данных

            :param validated_data: Данные, прошедшие валидацию
            :return: Созданный объект CompetencyProfileOfVacancy
            """

            CompetencyProfileOfVacancy = CompetencyProfileOfVacancy.objects.create(
                vacancy_name = validated_data['vacancy_name'],
                employer_id = validated_data['employer_id'],
                competencies_stack = validated_data['competencies_stack'],
                technology_stack = validated_data['technology_stack'],
                descr = validated_data['descr'],
            )

            return CompetencyProfileOfVacancy # Возвращаем созданный объект