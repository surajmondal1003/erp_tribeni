from django.contrib import admin
from django.urls import path
from rest_framework import routers
from attendance import views
from django.conf.urls import url, include

urlpatterns = [
    path('attendance', views.AttendanceView.as_view()),
]
