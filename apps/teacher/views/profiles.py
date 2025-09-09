from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.teacher.models import Teacher
from apps.teacher.serializers.profiles import TeacherCreateSerializer, TeacherDetailSerializer
from owerflow_core.permissions import IsAuthenticatedJWT, TenantScoped, IsSchoolAdmin

class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedJWT, TenantScoped, IsSchoolAdmin]
    lookup_field = "id"

    def get_queryset(self):
        return Teacher.objects.select_related("user").filter(school=self.request.tenant.school)

    def get_serializer_class(self):
        if self.action == "create":
            return TeacherCreateSerializer
        return TeacherDetailSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        instance = ser.save()
        out = TeacherDetailSerializer(instance)
        return Response(out.data, status=status.HTTP_201_CREATED)
