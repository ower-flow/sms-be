from django.urls import path
from apps.school.views import auth as auth_views

app_name = 'school'

urlpatterns = [
    path("auth/login", auth_views.SchoolLoginView.as_view(), name="school-login"),
]