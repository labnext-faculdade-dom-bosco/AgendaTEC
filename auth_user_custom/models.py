from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefone")
    notify_about_exams = models.BooleanField(default=True, verbose_name="Receber notificações de trabalhos e provas")
    notify_about_jobs = models.BooleanField(default=True, verbose_name="Receber notificações de vagas de emprego")