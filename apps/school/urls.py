from django.urls import path, re_path
from .views.auth import SchoolLoginView

app_name = 'school'

urlpatterns = [
    re_path(r"^auth/login/?$", SchoolLoginView.as_view(), name="login"),
]