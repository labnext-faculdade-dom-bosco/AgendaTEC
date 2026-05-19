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


@admin.register(AcademicContent)
class AcademicContentAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "colored_category",)
    search_fields = ("title", "description", "category",)
    list_filter = ("is_active",)
    formfield_overrides = {
        models.FileField: {
            'widget': forms.FileInput(attrs={'accept': 'application/pdf'})
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


@admin.register(AcademicFaq)
class AcademicFaqAdmin(admin.ModelAdmin):
    list_display = ("question", "answer",)
    search_fields = ("question", "answer",)
    list_filter = ("is_active",)


@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "contract_type",)
    search_fields = ("title", "description", "contract_type", )
    list_filter = ("is_active", "contract_type",)
