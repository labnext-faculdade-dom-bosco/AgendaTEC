from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Discipline, Event, Registration


class EventStudentsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.teacher = User.objects.create_user(username='teacher')
        cls.other_teacher = User.objects.create_user(username='other')
        cls.student = User.objects.create_user(username='student', first_name='Ana')
        cls.outsider = User.objects.create_user(username='outsider')
        professors = Group.objects.create(name='Professor')
        students = Group.objects.create(name='Aluno')
        cls.teacher.groups.add(professors)
        cls.other_teacher.groups.add(professors)
        cls.student.groups.add(students)
        cls.discipline = Discipline.objects.create(name='Web', teacher=cls.teacher)
        Registration.objects.create(student=cls.student, discipline=cls.discipline)
        cls.event = Event.objects.create(title='Trabalho', discipline=cls.discipline,
                                        event_date=timezone.now() + timedelta(days=1), event_local='Sala')
        cls.url = reverse('event-students', args=[cls.event.pk])

    def test_teacher_sees_only_enrolled_students(self):
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.get(self.url).json(), {'students': [{'name': 'Ana', 'completion': None}]})
        event = self.client.get(reverse('event-list')).json()[0]
        self.assertEqual(event['extendedProps']['students_url'], self.url)

    def test_other_teacher_cannot_see_event_or_read_roster(self):
        self.client.force_login(self.other_teacher)
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertEqual(self.client.get(reverse('event-list')).json(), [])

    def test_student_cannot_read_roster_or_see_button_link(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.assertIsNone(self.client.get(reverse('event-list')).json()[0]['extendedProps']['students_url'])

    def test_user_without_teacher_role_cannot_read_roster(self):
        self.client.force_login(self.outsider)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_anonymous_requires_login(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_student_only_sees_enrolled_discipline_events(self):
        other = Discipline.objects.create(name='Outra', teacher=self.other_teacher)
        Event.objects.create(title='Outro', discipline=other, event_date=timezone.now() + timedelta(days=1), event_local='Sala')
        self.client.force_login(self.student)
        self.assertEqual([event['title'] for event in self.client.get(reverse('event-list')).json()], ['Trabalho'])

    def test_admin_without_teacher_group_keeps_all_events(self):
        admin = get_user_model().objects.create_superuser(username='admin', password='test')
        self.client.force_login(admin)
        events = self.client.get(reverse('event-list')).json()
        self.assertEqual(len(events), 1)
        self.assertIsNone(events[0]['extendedProps']['students_url'])

    def test_empty_discipline(self):
        Registration.objects.all().delete()
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.get(self.url).json(), {'students': []})
