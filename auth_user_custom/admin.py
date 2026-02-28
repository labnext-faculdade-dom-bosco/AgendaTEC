from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Extras', {'fields': ('phone', 'notify_about_exams', 'notify_about_jobs')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Extras', {'fields': ('phone', 'notify_about_exams', 'notify_about_jobs')}),
    )

admin.site.register(User, UserAdmin)