from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
 ###signal setup
    def ready(self):
      import api.signals
