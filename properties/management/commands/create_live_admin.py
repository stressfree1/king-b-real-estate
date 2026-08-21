import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or reset the live admin account"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        email = os.environ.get("DJANGO_ADMIN_EMAIL")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not username:
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_ADMIN_USERNAME environment variable is missing."
                )
            )
            return

        if not email:
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_ADMIN_EMAIL environment variable is missing."
                )
            )
            return

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_ADMIN_PASSWORD environment variable is missing."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = email
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            message = "Live admin created successfully."
        else:
            message = "Live admin password and details reset successfully."

        self.stdout.write(
            self.style.SUCCESS(message)
        )