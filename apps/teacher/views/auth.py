from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.teacher.serializers.auth import TeacherLoginSerializer
from owerflow_core.auth.tokens import CustomRefreshToken
from owerflow_core.tenancy.resolver import get_current_tenant


@method_decorator(csrf_exempt, name="dispatch")
class TeacherLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "login"

    def post(self, request, *args, **kwargs):
        serializer = TeacherLoginSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        teacher = serializer.validated_data["teacher"]
        school = serializer.validated_data["school"]

        # Create custom token with teacher and school information
        refresh = CustomRefreshToken.for_user(user)
        # Include tenant claims so downstream services can enforce tenant boundaries
        refresh["school_id"] = school.id
        refresh["school_unique_id"] = school.unique_id
        refresh["teacher_id"] = teacher.id
        refresh["employee_id"] = teacher.employee_id
        
        # Add domain information if available from tenant
        try:
            tenant = get_current_tenant(request)
            if tenant and hasattr(tenant, 'schema_name'):
                refresh["domain"] = request.get_host()
        except Exception:
            pass

        return Response(
            {
                "school": {
                    "id": school.id,
                    "name": school.name,
                    "unique_id": school.unique_id,
                    "subscription_valid": school.is_subscription_valid,
                },
                "teacher": {
                    "id": teacher.id,
                    "employee_id": teacher.employee_id,
                    "email": teacher.email,
                    "full_name": teacher.full_name,
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
