from django.db import models

class SystemSettings(models.Model):
    """
    A singleton model to hold global system state and settings.
    Only one instance should be used.
    """
    # TODO Remove default values
    settings = models.CharField(max_length=50, default='system_state', unique=True)
    value = models.CharField(max_length=50, default='Log in')
