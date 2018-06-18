from django.contrib import admin
from django.urls import path
from rest_framework import routers
from authentication import views
from django.conf.urls import url, include
from .views import CustomObtainAuthToken



urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login', CustomObtainAuthToken.as_view()),
    path('create_user/', views.UserCreate.as_view()),
    path('all_employee/',views.EmployeeReadView.as_view()),
    path('all_employee/<pk>/',views.EmployeeReadDetailView.as_view()),
    path('employee/<pk>/', views.EmployeeMatserUpdate.as_view()),
    path('employee_dropdwon/', views.EmployeeDropdwon.as_view()),
]
