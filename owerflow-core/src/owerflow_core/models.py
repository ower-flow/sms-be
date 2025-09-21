from .enums import GenderEnum
from django.db import models
from django.core.validators import RegexValidator

import uuid

def avatar_upload_path(instance, filename):
    role = instance.__class__.__name__.lower()
    identifier = getattr(instance, "student_id", None) or getattr(instance, "teacher_id", None) or str(instance.pk)
    return f"{role}/avatars/{identifier}/{filename}"


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)

    class Meta:
        abstract = True

class BaseUserModel(BaseModel):
    
    # Identity
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=GenderEnum.choices,
        blank=False,
        null=False,
    )

    # Media
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        null=True,
        blank=True,
        verbose_name='Profile Picture',
        help_text='Upload your profile image (JPEG or PNG only).',
    )

    # Contact Info
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Enter a valid Pakistani mobile or PTCL landline number (e.g., +923001234567 or +924112345678)."
    )
    email = models.EmailField(unique=True)

    # National ID or CNIC or B-Form Number
    identity_number = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{7}-\d{1}$',
                message="CNIC must be in the format 00000-0000000-0."
            )
        ],
        help_text="Enter CNIC in format: 00000-0000000-0"
    )

    # Address
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

    # Association
    school = models.ForeignKey(
        'school.School',
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user is active. Unselect this instead of deleting."
    )

    class Meta:
        abstract = True
