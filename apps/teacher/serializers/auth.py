from rest_framework import serializers
from users.models import CustomUser
from apps.teacher.models import Teacher
from apps.school.models import School
from owerflow_core.enums import UserRoleEnum
from owerflow_core.tenancy.resolver import get_current_tenant, get_school_from_tenant
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


class TeacherLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    school_id = serializers.IntegerField(required=True)

    default_error_messages = {
        "invalid_credentials": "Invalid email or password.",
        "not_teacher": "Only teachers can log in here.",
        "teacher_not_in_school": "This teacher is not associated with the specified school.",
        "inactive_user": "This user account is inactive.",
        "inactive_school": "This school is inactive.",
        "expired_subscription": "School subscription has expired.",
        "school_not_found": "School not found.",
    }

    def validate(self, attrs):
        request = self.context.get("request")
        email = attrs.get("email", "").strip().lower()
        password = attrs.get("password")
        school_id = attrs.get("school_id")

        # Get the school
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            raise PermissionDenied(self.error_messages["school_not_found"])

        # Optional: If request comes from a tenant domain, validate school matches tenant
        if request:
            try:
                tenant = get_current_tenant(request)
                tenant_school = get_school_from_tenant(tenant)
                if tenant_school and tenant_school.id != school.id:
                    raise PermissionDenied("School ID does not match the current tenant's school.")
            except Exception:
                # If tenant resolution fails, continue with normal validation
                # This allows teacher login to work even without tenant context
                pass

        if not school.is_active:
            raise PermissionDenied(self.error_messages["inactive_school"])

        # Check subscription validity
        if not school.is_subscription_valid:
            raise PermissionDenied(self.error_messages["expired_subscription"])

        # Get the user
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed(self.error_messages["invalid_credentials"])

        if not user.is_active:
            raise PermissionDenied(self.error_messages["inactive_user"])

        if not user.check_password(password):
            raise AuthenticationFailed(self.error_messages["invalid_credentials"])

        # Check if user is a teacher
        if user.role != UserRoleEnum.TEACHER:
            raise PermissionDenied(self.error_messages["not_teacher"])

        # Check if teacher is associated with the specified school
        try:
            teacher = Teacher.objects.select_related('school').get(
                user=user, 
                school=school
            )
        except Teacher.DoesNotExist:
            raise PermissionDenied(self.error_messages["teacher_not_in_school"])

        attrs["user"] = user
        attrs["teacher"] = teacher
        attrs["school"] = school
        return attrs
