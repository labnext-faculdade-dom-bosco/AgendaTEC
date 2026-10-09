from allauth.account.signals import user_signed_up, user_logged_in
from django.contrib.auth.models import Group
from django.dispatch import receiver

from gvdasa.services import GvdasaService
from event.models import Discipline, Registration

def _get_user_group(email: str) -> str:
    prefix = email.split('@')[0]
    return "Aluno" if prefix.isdigit() else "Professor"

def _get_or_create_discipline(code, name):
    """ Busca a disciplina pelo código (identificador estável da GVDASA).
    Se não achar, tenta adotar uma disciplina legada com o mesmo nome mas
    sem código ainda (evita duplicar o que já existia antes do código existir).
    Também mantém o nome atualizado se ele mudar na origem. """
    discipline = Discipline.objects.filter(code=code).first()
    if discipline is None:
        discipline = Discipline.objects.filter(code__isnull=True, name=name).first()
        if discipline is not None:
            discipline.code = code
            discipline.save(update_fields=["code"])
        else:
            discipline = Discipline.objects.create(code=code, name=name)
    elif discipline.name != name:
        discipline.name = name
        discipline.save(update_fields=["name"])
    return discipline

def _set_disciplines_registration(user, disciplines_list):
    """ Atualiza o vínculo do aluno com as disciplinas cursadas """
    set_current_codes = set()
    for discipline in disciplines_list:
        discipline_code = discipline.get("Descricao", "").strip()
        discipline_name = discipline.get("DescricaoDisciplina", "").strip()
        if not discipline_code or not discipline_name:
            continue

        situation = discipline.get("SituacaoNaTurma")
        if situation not in ["Cursando"]:
            Registration.objects.filter(
                student=user,
                discipline__code=discipline_code,
            ).delete()
            continue

        discipline_obj = _get_or_create_discipline(discipline_code, discipline_name)
        Registration.objects.get_or_create(
            student=user,
            discipline=discipline_obj,
        )
        set_current_codes.add(discipline_code)

    Registration.objects.filter(
        student=user,
    ).exclude(
        discipline__code__in=set_current_codes,
    ).delete()

def _set_teacher_disciplines(user, turmas_list):
    """ Atualiza o vínculo do professor com as disciplinas que ministra """
    set_current_codes = set()
    for turma in turmas_list:
        discipline_code = turma.get("Descricao", "").strip()
        discipline_name = turma.get("DescricaoDisciplina", "").strip()
        if not discipline_code or not discipline_name:
            continue

        discipline = _get_or_create_discipline(discipline_code, discipline_name)
        if discipline.teacher_id != user.id:
            discipline.teacher = user
            discipline.save(update_fields=["teacher"])
        set_current_codes.add(discipline_code)

    Discipline.objects.filter(
        teacher=user,
    ).exclude(
        code__in=set_current_codes,
    ).update(teacher=None)

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

    if user.groups.filter(name="Professor").exists():
        teacher_data = gvdasa_service.get_teacher_info(user.email)
        if not teacher_data.get("ok"):
            return None

        turmas_list = teacher_data.get("data", {}).get("turmasperiodo", [])
        _set_teacher_disciplines(user, turmas_list)
        return None

    student_data = gvdasa_service.get_student_info(user.username)

    if not student_data.get("ok"):
        return None

    disciplines_list = student_data.get("data", {}).get("DisciplinasCursando", [])
    _set_disciplines_registration(user, disciplines_list)
