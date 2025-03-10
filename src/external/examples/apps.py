from django.apps import AppConfig

class ExamplesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.external.examples'
    label = 'examples'