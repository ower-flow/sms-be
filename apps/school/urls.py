from django.urls import path, re_path
from apps.school.views import auth as auth_views

app_name = 'school'

urlpatterns = [
    re_path("^auth/login/?$", auth_views.SchoolLoginView.as_view(), name="school-login"),
]