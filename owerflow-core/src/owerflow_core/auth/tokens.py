# owerflow_core/auth/tokens.py
import sys
from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        role = getattr(user, "role", None)
        token["role"] = role or None

        school_id = getattr(user, "_school_id", None)
        if school_id is None:
            if role == "ADMIN" and hasattr(user, "schooladmin") and user.schooladmin:
                school_id = user.schooladmin.school_id
            elif role == "TEACHER" and hasattr(user, "teacher_profile") and user.teacher_profile:
                school_id = user.teacher_profile.school_id
            elif role == "STUDENT" and hasattr(user, "student_profile") and user.student_profile:
                school_id = user.student_profile.school_id

        if school_id:
            token["school_id"] = school_id
        return token


def make_tokens_for_user(user, extra_claims: dict):
    refresh = CustomRefreshToken.for_user(user)
    for k, v in (extra_claims or {}).items():
        refresh[k] = v
    return str(refresh), str(refresh.access_token)
