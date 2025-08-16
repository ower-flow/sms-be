from django.test import TestCase
from django.db import IntegrityError
from core.apps.hyprd.models import HyprdUser
from core.apps.school.models import School, SchoolAdmin


class SchoolAdminTests(TestCase):
    def setUp(self):
        # Create a school instance for all tests
        self.school = School.objects.create(name='Test School', unique_id='TS001')

    def test_unique_school_admin(self):
        # Create the first school admin user
        first_admin_user = HyprdUser.objects.create_user(
            username='first_admin',
            email='first@test.com',
            password='first_password123',
            role='school_admin'
        )
        SchoolAdmin.objects.create(user=first_admin_user, school=self.school)

        # Attempt to create a second school admin for the same school
        second_admin_user = HyprdUser.objects.create_user(
            username='second_admin',
            email='second@test.com',
            password='second_password123',
            role='school_admin'
        )

        try:
            SchoolAdmin.objects.create(user=second_admin_user, school=self.school)
        except IntegrityError:
            print("IntegrityError raised as expected for duplicate school admin.")
            return  # Exit the test successfully if exception is raised

        # If no exception is raised, this line should be reached, indicating a failure
        self.fail("IntegrityError not raised for duplicate SchoolAdmin.")

