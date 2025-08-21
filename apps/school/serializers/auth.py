from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from users.models import CustomUser
from apps.school.models import School
from django_tenants.utils import get_tenant


class SchoolLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = CustomUser.objects.get(email=email, is_active=True)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_school_admin():
            raise serializers.ValidationError("Only school admins can log in here.")

        # domain restriction
        tenant = get_tenant(self.context["request"])
        school = getattr(tenant, "school", None)

        if school is None:
            raise serializers.ValidationError("No school is linked to this domain.")

        try:
            user_school = user.schooladmin.school
        except ObjectDoesNotExist:
            raise serializers.ValidationError("This user is not linked to any school.")

        if user_school.id != school.id:
            raise serializers.ValidationError("You are not authorized to use this domain.")

        # subscription validity
        if not school.is_subscription_valid:
            raise serializers.ValidationError("School subscription has expired.")

        data["user"] = user
        data["school"] = school
        return data
