from django.apps import AppConfig


class MyapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapi'

    def ready(self):
        from . import models
        system_state, _ = models.SystemSettings.objects.get_or_create(settings='system_state', defaults={'value': 'Log in'})
        system_state.value = 'Log in'
        system_state.save()
