from rest_framework.permissions import BasePermission
from .enums import UserRoleEnum

def _is_auth(u):
    return bool(u and u.is_authenticated and not u.is_superuser)

class IsAuthenticatedJWT(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsSuperuser(BasePermission):
    message = "Superuser access required."
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and u.is_superuser)

class IsSchoolAdmin(BasePermission):
    message = "School Admin access required."
    def has_permission(self, request, view):
        u = request.user
        return _is_auth(u) and getattr(u, "role", None) == UserRoleEnum.SCHOOL_ADMIN

class IsTeacher(BasePermission):
    message = "Teacher access required."
    def has_permission(self, request, view):
        u = request.user
        return _is_auth(u) and getattr(u, "role", None) == UserRoleEnum.TEACHER

class IsStudent(BasePermission):
    message = "Student access required."
    def has_permission(self, request, view):
        u = request.user
        return _is_auth(u) and getattr(u, "role", None) == UserRoleEnum.STUDENT

class TenantScoped(BasePermission):
    """
    User must belong to the current tenant's school.
    Public schema should not pass this check.
    """
    message = "You are not authorized for this tenant/domain."

    def has_permission(self, request, view):
        tenant = getattr(request, "tenant", None)
        school = getattr(tenant, "school", None)
        u = request.user

        if not (tenant and school and u and u.is_authenticated):
            return False

        role = getattr(u, "role", None)

        if role == UserRoleEnum.SCHOOL_ADMIN:
            admin_rel = getattr(u, "schooladmin", None)
            return bool(admin_rel and admin_rel.school_id == school.id)

        # if role == UserRoleEnum.TEACHER:
        #     teacher_rel = getattr(u, "teacher_profile", None)
        #     return bool(teacher_rel and teacher_rel.school_id == school.id)
        #
        # if role == UserRoleEnum.STUDENT:
        #     student_rel = getattr(u, "student_profile", None)
        #     return bool(student_rel and student_rel.school_id == school.id)

        return False
