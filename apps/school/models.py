from owerflow_core.enums import SchoolTypeEnum
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

import uuid

class School(models.Model):
    name = models.CharField(max_length=100)
    unique_id = models.SlugField(max_length=50, unique=True, db_index=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    established_year = models.PositiveIntegerField(null=True, blank=True)
    principal_name = models.CharField(max_length=100, null=True, blank=True)

    # Add these fields for better security
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    school_type = models.CharField(
        max_length=20,
        choices=SchoolTypeEnum.choices,
        null=True,
        blank=True
    )

    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)


    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return check_password(raw_password, self.password)


    def save(self, *args, **kwargs):
        # Hash password if it's not already hashed
        if self.password and not self.password.startswith(('pbkdf2_', 'bcrypt', 'argon2')):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.unique_id})"

    def clean(self):
        super().clean()
        
        # Subscription start or end date missing
        if bool(self.subscription_start_date) ^ bool(self.subscription_end_date):
            raise ValidationError("Both subscription start and end dates must be provided.")
        
            # Subscription validation
        if self.subscription_start_date and self.subscription_end_date:
            if self.subscription_start_date > self.subscription_end_date:
                raise ValidationError("Subscription start date cannot be later than the end date.")

        # Year logic
        if self.established_year:
            current_year = timezone.now().year
            if self.established_year > current_year:
                raise ValidationError("Established year cannot be in the future.")
            if self.established_year < 1800:
                raise ValidationError("Established year must be after 1800.")

    @property
    def is_subscription_valid(self):
        today = timezone.now().date()
        return (
            self.subscription_start_date and
            self.subscription_end_date and
            self.subscription_start_date <= today <= self.subscription_end_date
        )


    @property
    def subscription_duration(self):
        if self.subscription_start_date and self.subscription_end_date:
            return (self.subscription_end_date - self.subscription_start_date).days
        return None


class SchoolAdminModel(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='schooladmin')
    school = models.OneToOneField('school.School', on_delete=models.CASCADE)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Admin: {self.user.email} | School: {self.school.name}"

    def clean(self):
        """
        Ensures the associated HyprdUser has the correct role.
        """
        if self.user.role != 'schooladmin':
            raise ValidationError("The associated user must have the role 'schooladmin'.")
        super().clean()

    class Meta:
        verbose_name = "School Admin"
        verbose_name_plural = "School Admins"
        ordering = ['school__name']

