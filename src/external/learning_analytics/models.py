from django.db import models

class Technology(models.Model):
    """
    Модель Technology представляет ту или иную технологию, осваиваемую в процессе изучения дисциплин.

    Attributes:
        name (CharField): Название технологии. Максимальная длина — 60 символов.
        description (TextField): Описание технологии. Максимальная длина — 400 символов.
        popularity (PositiveIntegerField): Уровень популярности технологии.
        rating (IntegerField): Рейтинг технологии.
    """
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=400)
    popularity = models.PositiveIntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.description}"


class Competention(models.Model):
    """
    Модель Competention представляет компетенции.

    Attributes:
        code (CharField): Уникальный код компетенции. Максимальная длина — 10 символов.
        name (CharField): Название компетенции. Максимальная длина — 60 символов.
        description (TextField): Описание компетенции. Максимальная длина — 400 символов.
    """
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=400)

    def __str__(self):
        return f"{self.code} ({self.name})"