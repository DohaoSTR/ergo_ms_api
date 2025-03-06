# Импорт необходимых классов и модулей из Django REST Framework
from rest_framework.serializers import (
    ModelSerializer,  # Базовый класс для создания сериализаторов на основе моделей
    CharField,       # Поле для строковых данных
    BooleanField,    # Поле для булевых значений
    ValidationError, # Класс для обработки ошибок валидации
    Serializer       # Базовый класс для создания кастомных сериализаторов
)

# Импорт модели Technology из приложения learning_analytics
from src.external.learning_analytics.models import (
    Technology,
    Competention
)

# Создание сериализатора для модели Technology
class TechnologySerializer(ModelSerializer):
    class Meta:
        # Указываем модель, с которой работает сериализатор
        model = Technology
        # Указываем поля модели, которые будут сериализованы/десериализованы
        fields = ['name', 'description', 'popularity', 'rating']

        # Метод для создания нового объекта Technology
        def create(self, validated_data):
            """
            Создает новый объект Technology на основе валидированных данных.
            
            :param validated_data: Данные, прошедшие валидацию
            :return: Созданный объект Technology
            """
            technology = Technology.objects.create(
                name=validated_data['name'],          # Устанавливаем имя технологии
                description=validated_data['description'],  # Устанавливаем описание
                popularity=validated_data['popularity'],  # Устанавливаем популярность
                rating=validated_data['rating'],      # Устанавливаем рейтинг
            )
            return technology  # Возвращаем созданный объект

# Создание сериализатора для модели Competention
class CompetentionSerializer(ModelSerializer):
    class Meta:
        # Указываем модель, с которой работает сериализатор
        model = Competention
        # Указываем поля модели,которые будут сериализованы/десериализованы
        fields = ['code','name','description']

        def create(self, validated_data):
            """
            Создает новый объект Competention на основе валидированных данных.

            :param validated_data: Данные, прошедшие валидацию
            :return: Созданный объект Competention
            """ 

            competention = Competention.objects.create(
                code=validated_data['code'],                # Устанавливаем код компетенции
                name=validated_data['name'],                # Устанавливаем название компетенции
                description=validated_data['description']   # Устанавливаем описание компетенции
            )
            return competention # Возвращаем созданный объект