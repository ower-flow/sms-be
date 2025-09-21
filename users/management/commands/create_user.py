from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from owerflow_core.enums import GenderEnum
from users.models import RoleEnum


class Command(BaseCommand):
    help = "Creates a default Hyprd School Admin (not superuser)."

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = "fahad"
        email = "fahad@gmail.com"
        password = "7yhb#123"
        first_name = "Fahad"
        last_name = "Habib"
        phone_number = "+923000000000"
        address = "Shahkot HQ, Karachi"
        gender = GenderEnum.MALE
        role = RoleEnum.SCHOOL_ADMIN

        if not User.objects.filter(username=username).exists():
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                address=address,
                gender=gender,
                role=role,
                is_superuser=False,
                is_staff=False,
            )
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"School Admin user '{username}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
