from departments import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('all_departments/',views.DepartmentsReadView.as_view()),
    path('all_departments/<pk>/', views.DepartmentsReadDetailView.as_view()),
    path('departments/', views.DepartmentsMatser.as_view()),
    path('departments/<pk>/', views.DepartmentsUpdate.as_view()),
    path('departments_status/<pk>/', views.DepartmentsUpdateStatus.as_view()),
    path('company_departments/<company>/', views.SpecificCompanyDepartments.as_view()),
]