from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class Operator(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Фамилия")
    second_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")

    class Meta:
        verbose_name_plural = 'Операторы'
