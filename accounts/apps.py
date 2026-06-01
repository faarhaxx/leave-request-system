from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import os
        from django.conf import settings

        if getattr(settings, "CREATE_SUPERUSER", False):
            try:
                from .models import User

                if not User.objects.filter(username="admin").exists():
                    User.objects.create_superuser(
                        username="admin",
                        email="amanfarhan1234510@gmail.com",
                        password="weather123#"
                    )
            except Exception:
                pass