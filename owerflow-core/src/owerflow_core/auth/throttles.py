from rest_framework.throttling import SimpleRateThrottle

class LoginThrottle(SimpleRateThrottle):
    scope = "login"
    def get_cache_key(self, request, view):
        ip = request.META.get("REMOTE_ADDR") or ""
        email = (request.data.get("email") or "").lower()
        tenant = getattr(getattr(request, "tenant", None), "pk", "public")
        return f"login:{tenant}:{email}:{ip}"
