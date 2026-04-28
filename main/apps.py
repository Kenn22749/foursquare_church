from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import os

        if os.environ.get("RENDER"):
            try:
                from django.contrib.auth.models import User

                if not User.objects.filter(username="admin").exists():
                    User.objects.create_superuser(
                        username="Admin22church",
                        email="admin22fqchurch@gmail.com",
                        password="admin789123"
                    )
                    print("Temporary admin account created.")
            except Exception as e:
                print("Temporary admin creation skipped:", e)