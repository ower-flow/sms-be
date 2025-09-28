from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static


urlpatterns = [
   # path('admin/', admin.site.urls, name="admin"),
    path("api/v1/school/",  include("apps.school.urls",  namespace="school")),
    path("api/v1/teacher/", include("apps.teacher.urls", namespace="teacher")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)