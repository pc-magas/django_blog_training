from django.apps import AppConfig

class AppAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_auth'

    container = None

    def ready(self):
        from .container import Container  # import here, not at module top
        AppAuthConfig.container = Container()
        AppAuthConfig.container.wire(modules=[".views"])
        AppAuthConfig.container.wire(modules=[".admin"])