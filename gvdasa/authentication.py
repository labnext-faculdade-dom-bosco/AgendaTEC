import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from event.models import Discipline, Registration
from .services import GvdasaService
from .tools import extract_phone_number

_logger = logging.getLogger(__name__)

User = get_user_model()


class GvdasaBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
            Adiciona uma camada de lógica na autenticação padrão do Django.
            Quando o usuário não estiver cadastrado, é feita uma consulta na API e é criado um
            novo usuário no banco da aplicação usando a matrícula como login e também como senha.
            Esá implementação é genérica para o primeiro MVP, e no futuro será evoluída para que
            não seja necessário utilizar senha, e a autenticação seja da mesma forma que o Moodle
            está integrado no portal do aluno.
        """
        try:
            user = User.objects.get(username=username)
            user_data = None
        except User.DoesNotExist:
            user_data = self._get_student_information(registration=username)
            if not user_data:
                return None

            user_name = user_data.get("NumeroAluno")  # Matrícula
            contact_name = user_data.get("NomeAluno")
            phone_number = extract_phone_number(user_data.get("PessoaContatos"))

            user = self._create_user(user_name, contact_name, phone_number)
            self._assign_group(user, "Aluno")

        user_is_student = user.groups.filter(name="Aluno").exists()
        if not user_is_student:
            return None

        # Atualiza as disciplinas cursadas
        user_data = user_data or self._get_student_information(registration=username)
        if user_data:
            disciplines_list = user_data.get("DisciplinasCursando", [])
            self._set_disciplines_registration(user, disciplines_list)

        # Autenticação do usuário
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def _get_student_information(self, registration: str):
        gvdasa_service = GvdasaService()
        student_data = gvdasa_service.get_student_info(registration)

        student_exists = student_data.get("ok")
        if not student_exists:
            return None

        return student_data.get("data")

    def _create_user(self, user_name: str, contact_name: str, phone_number: str) -> User:
        try:
            user = User(
                username=user_name,
                first_name=contact_name,
                phone=phone_number,
                is_staff=True,
            )
            user.set_password(user_name)  # Senha temporária. Deve ser trocada no primeiro login
            user.save()
            return user
        except Exception as error:
            _logger.error(f"Erro ao criar usuário: {error}")
            return None

    def _assign_group(self, user: User, group_name: str) -> None:
        group_id, state = Group.objects.get_or_create(name=group_name)
        user.groups.add(group_id)

    def _set_disciplines_registration(self, user: User, disciplines_list: list) -> None:
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

            # Cria a disciplina quando ela não existir e matricula o aluno
            discipline_id, state = Discipline.objects.get_or_create(
                name=discipline_name,
                defaults={"is_active": True},
            )
            Registration.objects.get_or_create(
                student=user,
                discipline=discipline_id,
            )
            set_current_disciplines.add(discipline_name)

        # Remove o vínculo do aluno com disciplinas antigas
        Registration.objects.filter(
            student=user,
        ).exclude(
            discipline__name__in=set_current_disciplines,
        ).delete()
