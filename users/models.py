from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, UserManager
from django_tenants.models import TenantMixin, DomainMixin 
from owerflow_core.enums import GenderEnum


class RoleEnum(models.TextChoices):
    SCHOOL_ADMIN = 'schooladmin', 'School Admin'


class CustomUserManager(UserManager):
    """Custom manager for CustomUser model"""
    
    def school_admins(self):
        """Get all school admin users"""
        return self.filter(role=RoleEnum.SCHOOL_ADMIN)
    
    def active_users(self):
        """Get all active users"""
        return self.filter(is_active=True)
    
    def by_role(self, role):
        """Get users by specific role"""
        return self.filter(role=role, is_active=True)
    
    def superusers(self):
        """Get all superusers"""
        return self.filter(is_superuser=True)


class CustomUser(AbstractUser): 
    """Custom user model for SMS system"""
    
    role = models.CharField(
        max_length=20,  
        choices=RoleEnum.choices,
        blank=True,
        null=True,  # Allow null for superusers
        help_text="Role for regular users. Superusers don't need a role."
    )
    
    phone_number = models.CharField(
        max_length=20, 
        null=True, 
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?[\d\s\-\(\)]+$',  # More flexible regex for international numbers
                message="Please enter a valid phone number. Example: +92-300-1234567"
            )
        ],
        help_text="Enter phone number with country code. Example: +92-300-1234567"
    )
    
    address = models.TextField(
        null=True, 
        blank=True,
        help_text="Complete address of the user"
    )
    
    gender = models.CharField(
        max_length=10,
        choices=GenderEnum.choices,
        null=True,
        blank=True
    )
    
    # Profile image (optional)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        help_text="Profile picture of the user"
    )
    
    # Date fields
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Custom manager
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        """Override save to handle superuser role logic"""
        # Superuser does not have any role
        if self.is_superuser:
            self.role = None
        elif not self.role and not self.is_superuser:
            # Regular users have default role
            self.role = RoleEnum.SCHOOL_ADMIN
        
        super().save(*args, **kwargs)
    
    def clean(self):
        """Custom validation"""
        super().clean()
        
        # Email validation for school admin role
        if self.role == RoleEnum.SCHOOL_ADMIN and not self.email:
            raise ValidationError("Email is required for School Admin role.")
    
    def __str__(self):
        """String representation"""
        if self.is_superuser:
            return f"{self.username} (System Administrator)"
        
        role_display = self.get_role_display() if self.role else 'No Role'
        return f"{self.username} ({role_display})"
    
    def get_full_name_with_role(self):
        """Get full name with role"""
        full_name = self.get_full_name() or self.username
        if self.is_superuser:
            return f"{full_name} (System Admin)"
        elif self.role:
            return f"{full_name} ({self.get_role_display()})"
        return full_name
    
    def has_role_permission(self, required_role):
        """Check if user has required role or is superuser"""
        if self.is_superuser:
            return True
        return self.role == required_role
    
    def is_school_admin(self):
        """Check if user is school admin"""
        return self.role == RoleEnum.SCHOOL_ADMIN
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]


class SchoolSchema(TenantMixin):
    """
    Represents an isolated schema (tenant) for a specific school.
    Each school gets its own PostgreSQL schema for complete data isolation.
    """
    
    
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Created",
        help_text="The date when this school tenant was created."
    )
    
    
    school = models.OneToOneField(
        'school.School',
        on_delete=models.CASCADE,
        related_name="schema",
        verbose_name="Associated School",
        help_text="The school linked to this schema."
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this school schema is active"
    )
    
    # Tenant settings
    auto_create_schema = True
    # auto_drop_schema = False  # Safety: don't auto-delete schemas
    
    class Meta:
        verbose_name = "School Schema"
        verbose_name_plural = "School Schemas"
        ordering = ["-created_on"]
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['school']),
        ]
    
    # def clean(self):
    #     """Custom validation"""
    #     super().clean()
        
    #     # Check for duplicate school codes
    #     if self.school_code:
    #         existing = SchoolSchema.objects.filter(
    #             school_code=self.school_code
    #         ).exclude(pk=self.pk)
            
    #         if existing.exists():
    #             raise ValidationError(f"School code '{self.school_code}' already exists.")
    
    # def save(self, *args, **kwargs):
    #     """Override save with validation"""
    #     self.full_clean()
    #     super().save(*args, **kwargs)
    
    
    def clean(self):
        if SchoolSchema.objects.filter(school=self.school).exclude(pk=self.pk).exists():
            raise ValidationError("This school already has a schema.")

    def save(self, *args, **kwargs):
        self.full_clean()  # calls clean()
        super().save(*args, **kwargs)
    
    def get_domain_url(self):
        """Get primary domain URL"""
        primary_domain = self.domains.filter(is_primary=True).first()
        if primary_domain:
            return f"https://{primary_domain.domain}"
        return None
    
    def __str__(self):
        return f"{self.school.name if self.school else 'Unnamed School'} Schema"
    

class SchoolDomain(DomainMixin):
    """
    Represents a domain associated with a school tenant.
    Each tenant can have multiple domains (e.g., school1.example.com, custom-domain.com)
    """
    
    class Meta:
        verbose_name = "School Domain"
        verbose_name_plural = "School Domains"
        ordering = ['-is_primary', 'domain']
    
    