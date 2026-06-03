from django.apps import AppConfig


class AuthUserCustomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_user_custom'

    def ready(self):
        import auth_user_custom.signals
