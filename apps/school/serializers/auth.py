from rest_framework import serializers
from users.models import CustomUser
from django_tenants.utils import get_tenant
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


class SchoolLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    default_error_messages = {
        "invalid_credentials": "Invalid email or password.",
        "not_school_admin": "Only school admins can log in here.",
        "no_school_for_domain": "No school is linked to this domain.",
        "no_school_for_user": "This user is not linked to any school.",
        "wrong_domain": "You are not authorized to use this domain.",
        "expired_subscription": "School subscription has expired.",
        "inactive_user": "This user account is inactive.",
        "inactive_school": "This school is inactive.",
    }

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            raise PermissionDenied("Missing request context.")

        # Resolve current tenant from the domain (request.tenant if available)
        tenant = getattr(request, "tenant", None) or get_tenant(request)
        school = getattr(tenant, "school", None)
        if school is None:
            raise PermissionDenied(self.error_messages["no_school_for_domain"])

        email = attrs.get("email", "").strip().lower()
        password = attrs.get("password")

        try:
            # Pull the related school via SchoolAdminModel
            user = (
                CustomUser.objects
                .select_related("schooladmin__school")
                .get(email=email)
            )
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed(self.error_messages["invalid_credentials"])

        if not user.is_active:
            raise PermissionDenied(self.error_messages["inactive_user"])

        if not user.check_password(password):
            raise AuthenticationFailed(self.error_messages["invalid_credentials"])

        if not user.is_school_admin():
            raise PermissionDenied(self.error_messages["not_school_admin"])

        try:
            user_school = user.schooladmin.school
        except ObjectDoesNotExist:
            raise PermissionDenied(self.error_messages["no_school_for_user"])

        if not school.is_active:
            raise PermissionDenied(self.error_messages["inactive_school"])

        # Enforce domain/school match
        if user_school.id != school.id:
            raise PermissionDenied(self.error_messages["wrong_domain"])

        # Subscription validity on the domain’s school
        if not school.is_subscription_valid:
            raise PermissionDenied(self.error_messages["expired_subscription"])

        attrs["user"] = user
        attrs["school"] = school
        attrs["schema"] = tenant.schema_name
        attrs["domain"] = request.get_host()
        return attrs
