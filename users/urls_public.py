from .views import index
from django.urls import path
from django.contrib import admin

app_name = "users"

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls, name="admin"),
]