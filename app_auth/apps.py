from django.apps import AppConfig
from app_auth import container

class AppAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_auth'

    def ready(self):
        container.wire(modules=[".views"])