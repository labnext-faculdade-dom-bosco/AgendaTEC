from django.db import models
from django import forms
from django.utils.html import format_html
from django.contrib import admin
from academic.models import AcademicContent, AcademicFaq, JobOpportunity

CATEGORY_COLORS = {
    "matriz_ads": "#4A90D9",
    "matriz_si":  "#7B68EE",
    "horas_comp": "#F5A623",
    "info_inst":  "#7ED321",
}


class PdfClearableFileInput(forms.ClearableFileInput):
    """ ClearableFileInput com o link do arquivo atual estilizado como botão
    (em vez do texto "Atualmente: <caminho interno>" padrão do Django). """
    template_name = "academic/widgets/pdf_clearable_file_input.html"


@admin.register(AcademicContent)
class AcademicContentAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "colored_category", "pdf_link",)
    search_fields = ("title", "description", "category",)
    list_filter = ()
    formfield_overrides = {
        models.FileField: {
            'widget': PdfClearableFileInput(attrs={'accept': 'application/pdf'})
        },
    }

    def colored_category(self, obj):
        color = CATEGORY_COLORS.get(obj.category, "#999")
        label = obj.get_category_display()
        return format_html(
            "<span style='background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600'>{}</span>",
            color, label
        )

    colored_category.short_description = "Categoria"

    def pdf_link(self, obj):
        if not obj.pdf_file:
            return "-"
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">Abrir arquivo</a>',
            obj.pdf_file.url,
        )

    pdf_link.short_description = "Arquivo"


@admin.register(AcademicFaq)
class AcademicFaqAdmin(admin.ModelAdmin):
    list_display = ("question", "answer",)
    search_fields = ("question", "answer",)
    list_filter = ()


@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "contract_type",)
    search_fields = ("title", "description", "contract_type", )
    list_filter = ("contract_type",)
