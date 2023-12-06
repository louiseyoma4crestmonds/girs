from django.apps import AppConfig
from django.utils.translation import gettext_lazy as lazy_text


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # Plug signal.py into application so that it is accessible anywhere
    def ready(self):
        import api.signals
