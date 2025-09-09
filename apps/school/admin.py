from django.contrib import admin
from .models import School, SchoolAdminModel


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unique_id', 'city', 'state', 'contact_number', 'email',)
    list_filter = ('state', 'city')
    search_fields = ('name', 'unique_id', 'city', 'email', 'contact_number')
    ordering = ('name',)
    readonly_fields = ('is_subscription_valid', 'subscription_duration')

    fieldsets = (
        (None, {
            'fields': ('name', 'unique_id', 'address', 'city', 'state', 'zipcode')
        }),
        ('Contact Info', {
            'fields': ('contact_number', 'email')
        }),
        ('Subscription Details', {
            'fields': ('subscription_start_date', 'subscription_end_date', 'is_subscription_valid', 'subscription_duration')
        }),
        ('School Details', {
            'fields': ('established_year', 'principal_name',)
        }),
    )


@admin.register(SchoolAdminModel)
class SchoolAdminModelAdmin(admin.ModelAdmin):
    list_display = ('school', 'created_at')
    list_filter = ('school__city', 'school__state')
    search_fields = ('school__name',)
    ordering = ('school__name',)

    fieldsets = (
        ('Relationships', {
            'fields': ('user', 'school')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

