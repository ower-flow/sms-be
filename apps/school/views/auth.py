from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.school.serializers.auth import SchoolLoginSerializer
from apps.school.tokens import CustomRefreshToken

@method_decorator(csrf_exempt, name="dispatch")
class SchoolLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "login"

    def post(self, request, *args, **kwargs):
        serializer = SchoolLoginSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        school = serializer.validated_data["school"]
        # schema = serializer.validated_data["schema"]
        domain = serializer.validated_data["domain"]

        # Update last_login fields atomically
        with transaction.atomic():
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
            school.last_login = timezone.now()
            school.save(update_fields=["last_login"])

        refresh = CustomRefreshToken.for_user(user)
        # Include tenant claims so downstream services can enforce tenant boundaries
        refresh["school_id"] = school.id
        refresh["school_unique_id"] = school.unique_id
        refresh["domain"] = domain

        return Response(
            {
                "school": {
                    "id": school.id,
                    "name": school.name,
                    "unique_id": school.unique_id,
                    "subscription_valid": school.is_subscription_valid,
                },
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_200_OK,
        )
