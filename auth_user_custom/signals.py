from allauth.account.signals import user_signed_up, user_logged_in
from django.contrib.auth.models import Group
from django.dispatch import receiver

from gvdasa.services import GvdasaService
from event.models import Discipline, Registration

def _get_user_group(email: str) -> str:
    prefix = email.split('@')[0]
    return "Aluno" if prefix.isdigit() else "Professor"

def _set_disciplines_registration(user, disciplines_list):
    """ Atualiza o vínculo do aluno com as disciplinas cursadas """
    set_current_disciplines = set()
    for discipline in disciplines_list:
        discipline_name = discipline.get("DescricaoDisciplina", "").strip()
        if not discipline_name:
            continue

        situation = discipline.get("SituacaoNaTurma")
        if situation not in ["Cursando"]:
            Registration.objects.filter(
                student=user,
                discipline__name=discipline_name,
            ).delete()
            continue

        discipline_id, _ = Discipline.objects.get_or_create(
            name=discipline_name,
            defaults={"is_active": True},
        )
        Registration.objects.get_or_create(
            student=user,
            discipline=discipline_id,
        )
        set_current_disciplines.add(discipline_name)

    Registration.objects.filter(
        student=user,
    ).exclude(
        discipline__name__in=set_current_disciplines,
    ).delete()

@receiver(user_signed_up)
def set_user_staff_on_signup(sender, request, user, **kwargs):
    user.is_staff = True
    user.save()

    group_name = _get_user_group(user.email)
    group, state = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)


@receiver(user_logged_in)
def on_user_login(sender, request, user, sociallogin=None, **kwargs):
    if sociallogin is None:  # login por usuário/senha
        return None

    gvdasa_service = GvdasaService()
    student_data = gvdasa_service.get_student_info(user.username)

    if not student_data.get("ok"):
        return None

    disciplines_list = student_data.get("data", {}).get("DisciplinasCursando", [])
    _set_disciplines_registration(user, disciplines_list)
