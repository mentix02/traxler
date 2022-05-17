from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from user.signals import create_user_info_and_token
