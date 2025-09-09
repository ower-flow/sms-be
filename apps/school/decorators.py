from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def tenant_required(view_func):
    """
    Decorator to check if the current tenant matches the school tenant of the logged-in user.
    Must be called with `user` explicitly passed.
    """
    @wraps(view_func)
    def _wrapped_view(self, user, *args, **kwargs):
        if user and hasattr(user, 'schooladmin'):
            current_tenant = getattr(self.request, 'tenant', None)
            school_tenant = user.schooladmin.school.schema

            print(f"Authenticated User: {user}")
            print(f"Current Tenant: {current_tenant}, School Tenant: {school_tenant}")

            if current_tenant and school_tenant == current_tenant:
                return view_func(self, user, *args, **kwargs)

            messages.error(self.request, "You are not authorized to access this school.")
        else:
            messages.error(self.request, "Invalid user or school association.")

        return redirect('school:login')

    return _wrapped_view
