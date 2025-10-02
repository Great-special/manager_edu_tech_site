# myapp/management/commands/createsu.py
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        superusers = os.getenv("superusers")
        if superusers:
            for su in superusers:
                if not User.objects.filter(username=os.getenv(su["DJANGO_SUPERUSER_USERNAME"])).exists():
                    User.objects.create_superuser(
                        username=os.getenv(su["DJANGO_SUPERUSER_USERNAME"]),
                        email=os.getenv(su["DJANGO_SUPERUSER_EMAIL"]),
                        password=os.getenv(su["DJANGO_SUPERUSER_PASSWORD"]),
                        first_name=os.getenv(su["DJANGO_SUPERUSER_FIRSTNAME"]),
                        last_name=os.getenv(su["DJANGO_SUPERUSER_LASTNAME"])
                    )
                    self.stdout.write(self.style.SUCCESS("Superuser created"))
