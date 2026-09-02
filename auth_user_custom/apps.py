from django.apps import AppConfig


class AuthUserCustomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_user_custom'
    verbose_name = 'Usuários'

    def ready(self):
        import auth_user_custom.signals
        self._hide_unused_admin_sections()
        self._merge_users_into_auth_group()

    @staticmethod
    def _hide_unused_admin_sections():
        """ Remove do Django Admin as seções usadas só internamente: "Contas" e
        "Contas sociais" do allauth (integração de login com a Microsoft),
        "Sites", exigido pelo allauth mas sem uso direto pelo usuário, e os
        models de agendamento do django_celery_beat que não são "Tarefas
        Periódicas" (só essa precisa aparecer no menu). """
        from django.contrib import admin
        from django.contrib.sites.models import Site
        from allauth.account.models import EmailAddress
        from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
        from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, SolarSchedule

        models_to_hide = (
            EmailAddress, SocialAccount, SocialApp, SocialToken, Site,
            ClockedSchedule, CrontabSchedule, IntervalSchedule, SolarSchedule,
        )
        for model in models_to_hide:
            try:
                admin.site.unregister(model)
            except admin.sites.NotRegistered:
                pass

    @staticmethod
    def _merge_users_into_auth_group():
        """ Exibe "Usuários" (auth_user_custom) dentro da mesma seção do menu
        que "Grupos" (auth), em vez de uma seção separada no menu lateral. """
        import types
        from django.contrib import admin

        original_get_app_list = admin.AdminSite.get_app_list

        def get_app_list(self, request, app_label=None):
            app_list = original_get_app_list(self, request, app_label)
            auth_app = next((a for a in app_list if a['app_label'] == 'auth'), None)
            users_app = next((a for a in app_list if a['app_label'] == 'auth_user_custom'), None)
            if auth_app and users_app:
                auth_app['models'].extend(users_app['models'])
                auth_app['models'].sort(key=lambda m: m['name'])
                app_list.remove(users_app)
            return app_list

        admin.site.get_app_list = types.MethodType(get_app_list, admin.site)
