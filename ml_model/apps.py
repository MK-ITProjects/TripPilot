from django.apps import AppConfig


class MlModelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml_model'
    verbose_name = 'ML Model'
