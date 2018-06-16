from django.contrib import admin
from django.urls import path
from rest_framework import routers
from attendance import views
from django.conf.urls import url, include

urlpatterns = [
    path('attendance/', views.AttendanceView.as_view()),
    path('attendance/<pk>/', views.AttendanceUpadteView.as_view()),
    path('emp_attendance/<emp>/', views.SpecificEmployeeAttendanceView.as_view()),
]
