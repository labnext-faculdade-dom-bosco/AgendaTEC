from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from event.models import Event, Discipline, Registration, CalendarModelView


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    search_fields = ('title',)
    list_filter = ('is_active',)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'discipline',)
    search_fields = ('student',)
    list_filter = ('is_active',)


@admin.register(CalendarModelView)
class CalendarViewAdmin(admin.ModelAdmin):
    template_name = "event/calendar.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("calendar/", self.admin_site.admin_view(self.get_calendar_view), name='calendar'),
        ]
        return custom_urls + urls

    def get_calendar_view(self, request, *args, **kwargs):
        context = {
            **self.admin_site.each_context(request),
            "title": "Calendário",
        }
        return render(request, self.template_name, context=context)

    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect('calendar/')
