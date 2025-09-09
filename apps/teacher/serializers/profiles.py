# apps/teacher/serializers.py
from rest_framework import serializers
from django.db import transaction
from users.models import CustomUser
from owerflow_core.enums import UserRoleEnum
from apps.teacher.models import Teacher

class TeacherCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    employee_id = serializers.CharField()

    def validate(self, attrs):
        # Optionally: check if a user with this email already exists in this tenant
        # If you keep global unique email = False, you may still want to prohibit duplicate users within the same school.
        return attrs

    @transaction.atomic
    def create(self, attrs):
        request = self.context["request"]
        school = request.tenant.school

        # Create or fetch the user (decide your policy; here we create new)
        user = CustomUser(
            username=attrs["email"],  # or any scheme you prefer
            email=attrs["email"],
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
            role=UserRoleEnum.TEACHER,
            is_active=True,
        )
        user.set_password(attrs["password"])
        user.save()

        teacher = Teacher.objects.create(
            user=user,
            school=school,
            employee_id=attrs["employee_id"],
        )
        return teacher

class TeacherDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Teacher
        fields = ["id", "employee_id", "email", "first_name", "last_name", "full_name"]
