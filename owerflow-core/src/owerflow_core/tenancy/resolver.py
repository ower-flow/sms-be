from django_tenants.utils import get_tenant as dt_get_tenant

def get_current_tenant(request):
    return getattr(request, "tenant", None) or dt_get_tenant(request)

def get_school_from_tenant(tenant):
    return getattr(tenant, "school", None) or tenant
