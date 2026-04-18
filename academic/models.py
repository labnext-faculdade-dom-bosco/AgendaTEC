from django.db import models
from django.conf import settings


class AcademicContent(models.Model):
    CATEGORY_CHOICES = [
        ("matriz_ads", "Matriz Curricular - ADS"),
        ("matriz_si", "Matriz Curricular - SI"),
        ("horas_comp", "Horas Complementares"),
        ("info_inst", "Informações Institucionais"),
    ]

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        verbose_name="Categoria",
    )
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
    pdf_file = models.FileField(upload_to='academic_files/', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Conteúdo Acadêmico"
        verbose_name_plural = "Conteúdo Acadêmico"

    def __str__(self):
        return self.title


class AcademicFaq(models.Model):
    question = models.CharField(max_length=500, verbose_name="Pergunta")
    answer = models.TextField(verbose_name="Respota")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"

    def __str__(self):
        return self.question
