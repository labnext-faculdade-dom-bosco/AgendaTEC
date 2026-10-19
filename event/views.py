from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.http import JsonResponse
from django.urls import reverse
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
                    "students_url": (
                        reverse('event-students', args=[event.pk])
                        if user.groups.filter(name="Professor").exists()
                        and not user.groups.filter(name="Aluno").exists()
                        else None
                    ),
                }
            })

        return JsonResponse(event_list, safe=False)


class EventStudentsView(LoginRequiredMixin, generic.View):
    def get(self, request, pk):
        user = request.user
        if not user.groups.filter(name="Professor").exists() or user.groups.filter(name="Aluno").exists():
            return JsonResponse({"error": "Acesso restrito aos professores."}, status=403)
        event = get_object_or_404(Event, pk=pk, discipline__teacher=user)
        students = event.discipline.students.order_by('first_name', 'last_name', 'username')
        return JsonResponse({"students": [
            {"name": student.get_full_name() or student.username, "completion": None}
            for student in students
        ]})
