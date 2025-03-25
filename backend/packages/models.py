from django.db import models


class Client(models.Model):
    """Модель клиентов (отправитель/получатель)"""
    name = models.CharField()
