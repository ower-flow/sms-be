
from django.urls import path
from . import views

app_name = 'teacher'

from rest_framework.routers import DefaultRouter
from apps.teacher.views.profiles import TeacherViewSet

router = DefaultRouter()
router.register(r"teachers", TeacherViewSet, basename="teacher")
urlpatterns = router.urls


urlpatterns = []
