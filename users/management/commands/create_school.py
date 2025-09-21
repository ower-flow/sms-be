from django.core.management.base import BaseCommand
from apps.school.models import School
from owerflow_core.enums import SchoolTypeEnum
from datetime import date


class Command(BaseCommand):
    help = "Creates a school record (no user or admin link)."

    def handle(self, *args, **kwargs):
        # School data
        school_name = "Decent Public School"
        unique_id = "21-DHS-2023"
        email = "decent@school.com"
        contact_number = "+923000000111"
        address = "Bahria Town, Lahore"
        city = "Lahore"
        state = "Punjab"
        zipcode = "54000"
        principal_name = "Dr. Fahad"
        established_year = 2021
        school_type = SchoolTypeEnum.HIGH_SCHOOL
        # subscription_status = True
        subscription_start = date(2024, 1, 1)
        subscription_end = date(2025, 1, 1)

        # Create school
        school, created = School.objects.get_or_create(
            unique_id=unique_id,
            defaults={
                "name": school_name,
                "email": email,
                "contact_number": contact_number,
                "address": address,
                "city": city,
                "state": state,
                "zipcode": zipcode,
                "principal_name": principal_name,
                "established_year": established_year,
                "school_type": school_type,
                "subscription_start_date": subscription_start,
                "subscription_end_date": subscription_end,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"School '{school_name}' created successfully."))
        else:
            self.stdout.write(self.style.WARNING(f"School '{school_name}' already exists."))
