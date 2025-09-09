import sys
from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        # minimal claims
        token["role"] = user.role or None

        school_id = None
        if hasattr(user, "schooladmin") and user.schooladmin:
            school_id = user.schooladmin.school_id
        elif hasattr(user, "teacher_profile") and user.teacher_profile:
            school_id = user.teacher_profile.school_id
        elif hasattr(user, "student_profile") and user.student_profile:
            school_id = user.student_profile.school_id

        if school_id:
            token["school_id"] = school_id

        # DEBUG: print to stdout (safe in dev)
        sys.stdout.write(
            f"[DEBUG] Issuing token for user_id={getattr(user, 'id', None)} "
            f"email={getattr(user, 'email', None)} "
            f"role={user.role} "
            f"school_id={school_id}\n"
        )

        return token
