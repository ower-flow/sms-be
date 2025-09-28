
from django.urls import path, re_path
from apps.teacher.views.auth import TeacherLoginView

app_name = 'teacher'

urlpatterns = [
    path('auth/login/', TeacherLoginView.as_view(), name='teacher-login'),
]
