from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from apps.school.serializers.auth import SchoolLoginSerializer


class SchoolLoginView(APIView):
    permission_classes = []  # Public endpoint

    def post(self, request, *args, **kwargs):
        serializer = SchoolLoginSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        school = serializer.validated_data["school"]

        # Update last_login
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        school.last_login = timezone.now()
        school.save(update_fields=["last_login"])

        refresh = RefreshToken.for_user(user)

        return Response({
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
            }
        }, status=status.HTTP_200_OK)
