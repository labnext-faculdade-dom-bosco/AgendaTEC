from django.contrib import admin
from academic.models import AcademicContent, AcademicFaq, JobOportunity


@admin.register(AcademicContent)
class AcademicContentAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category",)
    search_fields = ("title", "description", "category",)
    list_filter = ("is_active",)


@admin.register(AcademicFaq)
class AcademicFaqAdmin(admin.ModelAdmin):
    list_display = ("question", "answer",)
    search_fields = ("title", "description",)
    list_filter = ("is_active",)


@admin.register(JobOportunity)
class JobOportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "contract_type",)
    search_fields = ("title", "description", "contract_type", )
    list_filter = ("is_active", "contract_type",)
