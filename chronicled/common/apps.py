from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chronicled.common'

    def ready(self):
        import chronicled.profiles.signals
