from django.apps import AppConfig

class AnalyzeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'external.ETL.analyze'  # Или просто 'ETL.analyze', если проект работает из корня
