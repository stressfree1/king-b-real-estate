from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or reset the live admin account"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = "admin"
        password = "WEEKEND32"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Live admin {'created' if created else 'password reset'} successfully."
            )
        )