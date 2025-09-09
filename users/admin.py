from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import CustomUser, SchoolSchema, SchoolDomain, RoleEnum


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Enhanced admin for CustomUser"""
    
    list_display = [
        'username', 
        'email', 
        'get_full_name_display',
        'get_role_display_admin', 
        'phone_number',
        'is_active', 
        'is_superuser',
        'created_at'
    ]
    
    list_filter = [
        'is_active', 
        'is_superuser', 
        'role', 
        'gender',
        'is_staff',
        'created_at'
    ]
    
    search_fields = [
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'phone_number'
    ]
    
    ordering = ['-created_at']
    
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Personal Information', {
            'fields': (
                'phone_number', 
                'address', 
                'gender', 
                'date_of_birth',
                'profile_image'
            )
        }),
        ('Role & Permissions', {
            'fields': ('role',),
            'description': 'Note: Superusers do not need a role assigned.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # fields for creating new users
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Personal Information', {
            'fields': (
                'email',
                'first_name',
                'last_name',
                'phone_number', 
                'address', 
                'gender',
                'date_of_birth'
            )
        }),
        ('Role Assignment', {
            'fields': ('role',),
            'description': 'Leave empty for superusers'
        }),
    )
    
    def get_full_name_display(self, obj):
        """Display full name or username"""
        return obj.get_full_name() or obj.username
    get_full_name_display.short_description = 'Full Name'
    
    def get_role_display_admin(self, obj):
        """Custom role display with colors"""
        if obj.is_superuser:
            return format_html(
                '<strong style="color: #dc3545;">System Administrator</strong>'
            )
        elif obj.role == RoleEnum.SCHOOL_ADMIN:
            return format_html(
                '<span style="color: #28a745;">School Admin</span>'
            )
        elif obj.role:
            return obj.get_role_display()
        else:
            return format_html('<span style="color: #ffc107;">No Role</span>')
    
    get_role_display_admin.short_description = 'Role'
    get_role_display_admin.admin_order_field = 'role'


@admin.register(SchoolSchema)
class SchoolSchemaAdmin(admin.ModelAdmin):
    
    list_display = [
        'schema_name', 
        'school', 
        'is_active',
        'created_on'
    ]
    
    list_filter = [
        'school', 
        'is_active', 
        'created_on'
    ]
    
    search_fields = [
        'schema_name', 
    ]
    
    ordering = ['-created_on']
    
    readonly_fields = ['created_on',]
    
    def has_add_permission(self, request):
        """Only superusers can create tenants"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete tenants"""
        return request.user.is_superuser
    
    def save_model(self, request, obj, form, change):
        """Auto-generate schema_name if not provided"""
        if not obj.schema_name and obj.school_code:
            obj.schema_name = obj.school_code.lower().replace(' ', '_')
        super().save_model(request, obj, form, change)


@admin.register(SchoolDomain)
class SchoolDomainAdmin(admin.ModelAdmin):
    """Enhanced admin for SchoolDomain"""
    
    list_display = [
        'domain', 
        'is_primary',
    ]
    
    list_filter = [
        'is_primary',
    ]
    
    search_fields = [
        'domain', 
    ]
    
    ordering = ['-is_primary', 'domain']
    
    def has_add_permission(self, request):
        """Only superusers can add domains"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Only superusers can delete domains"""
        return request.user.is_superuser


# Custom admin site configuration
admin.site.site_header = "SMS - School Management System"
admin.site.site_title = "SMS Admin"
admin.site.index_title = "Welcome to School Management System"
