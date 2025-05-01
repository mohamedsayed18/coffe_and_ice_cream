from django.db import models


class SystemSettings(models.Model):
    settings = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)


class Items(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    date = models.DateField()
