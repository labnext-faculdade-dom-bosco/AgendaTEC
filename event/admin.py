from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from event.models import Event, Discipline, Registration, CalendarModelView
from event.forms import ExcelImportForm
from django.utils import timezone
from datetime import datetime
import openpyxl


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

    change_list_template = "event/event_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('excel-import/', self.admin_site.admin_view(self.view_excel_import), name='excel_import'),
        ]
        return custom_urls + urls

    def view_excel_import(self, request):
        form = ExcelImportForm()

        if request.method == 'POST':
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                wb = openpyxl.load_workbook(request.FILES['file'])
                ws = wb.active

                errors = []
                for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                    title = row[0]
                    description = row[1]
                    event_date_str = row[2]
                    event_local = row[3]
                    discipline_name = row[4]

                    # Validação de data
                    event_date = datetime.strptime(event_date_str, "%Y-%m-%d %H:%M")
                    event_date = timezone.make_aware(event_date)
                    if event_date and event_date.date() < timezone.localdate():
                        errors.append(f"Linha {i}: data no passado ({event_date.strftime('%d/%m/%Y')})")
                        continue

                    try:
                        discipline = Discipline.objects.get(name=discipline_name)
                    except Discipline.DoesNotExist:
                        errors.append(f"Linha {i}: disciplina '{discipline_name}' não encontrada")
                        continue

                    Event.objects.create(
                        title=title,
                        description=description,
                        event_date=event_date,
                        event_local=event_local,
                        discipline=discipline,
                        is_active=True,
                    )

                # Adiciona as mensagens de erro ao template
                if errors:
                    form.add_error(None, f"Algumas linhas foram ignoradas: {'; '.join(errors)}")
                else:
                    return redirect('admin:event_event_changelist')

        context = {
            **self.admin_site.each_context(request),  # mantém sidebar, usuário etc.
            "form": form,
            "title": "Importar Excel",
            "opts": self.model._meta,  # mantém o breadcrumb correto
        }
        return render(request, 'event/excel_import.html', context)


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
