from django.shortcuts import render
from django.views import generic
from django.shortcuts import render
from django.http import JsonResponse
from .models import Event


class CalendarView(generic.View):
    template_name = "event/calendar.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EventListView(generic.View):
    def get(self, request, *args, **kwargs):
        """
            Retorna os eventos de acordo com o perfil do usuário.

            Admin:      Todos os eventos
            Professor:  Somente eventos das disciplinas que ministra
            Aluno:      Somente eventos das disciplinas que está cursando
        """

        user = request.user
        if user.groups.filter(name="Aluno").exists():
            events = Event.objects.filter(discipline__students=user)
        elif user.groups.filter(name="Professor").exists():
            events = Event.objects.filter(discipline__teacher=user)
        else:
            events = Event.objects.all()

        event_list = []

        for event in events:
            event_list.append({
                "title": event.title,
                "start": event.event_date.isoformat(),
                "description": event.description,
                "extendedProps": {
                    "event_local": event.event_local,
                    "discipline": event.discipline.name,
                }
            })

        return JsonResponse(event_list, safe=False)
