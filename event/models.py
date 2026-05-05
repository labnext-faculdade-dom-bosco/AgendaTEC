from django.db import models
from auth_user_custom.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Discipline(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Nome")
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    teacher = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Professor(a)")
    students = models.ManyToManyField(
        User,
        through='Registration',
        related_name='disciplines',
        verbose_name='Disciplinas'
    )

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100, blank=False, verbose_name="Título")
    description = models.TextField(null=True, blank=True, verbose_name="Descrição")
    event_date = models.DateTimeField(verbose_name="Data e hora do evento")
    event_local = models.TextField(verbose_name="Local do evento")
    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT, verbose_name="Disciplina")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.title

    def clean(self):
        if self.event_date and (self.event_date < timezone.now()):
            raise ValidationError({"event_date": "A data não pode ser no passado."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Aluno")
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name="Disciplina")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        unique_together = ('student', 'discipline')

    def __str__(self):
        return f"{self.student} - {self.discipline}"


class CalendarModelView(models.Model):
    class Meta:
        managed = False  # Não cria tabela no banco
        verbose_name = "Calendário"
