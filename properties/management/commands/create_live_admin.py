import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create the live admin account if it does not already exist"

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

        user = User.objects.filter(username=username).first()

        if user:
            self.stdout.write(
                self.style.WARNING(
                    f"Admin user '{username}' already exists. "
                    "No changes were made."
                )
            )
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Live admin '{user.username}' created successfully."
            )
        )