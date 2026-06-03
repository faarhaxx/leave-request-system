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

                users = [
                    ("admin", "amanfarhan1234510@gmail.com", "weather123#", True, True),
                    ("employee1", "", "confirmation123#", False, False),
                    ("manager1", "", "authentication123#", False, False),
                ]

                for username, email, password, is_staff, is_superuser in users:
                    user, created = User.objects.get_or_create(
                        username=username,
                        defaults={"email": email}
                    )

                    user.set_password(password)
                    user.is_active = True
                    user.is_staff = is_staff
                    user.is_superuser = is_superuser
                    user.save()

            except Exception:
                pass