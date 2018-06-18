from django.contrib import admin
from django.urls import path
from rest_framework import routers
from appapprovepermission import views
from django.conf.urls import url, include

urlpatterns = [
    path('app_approve/', views.AppApproveView.as_view()),
    path('emp_approve/', views.EmpAppApproveView.as_view()),
    path('all_emp_approve/', views.EmpAppApproveReadView.as_view()),
    path('all_emp_approve/<pk>/', views.EmpAppDetailApproveReadView.as_view()),
    path('emp_approve/<pk>/', views.EmpAppApproveUpadteView.as_view()),
    path('content_dropdown/', views.ContentDropdown.as_view()),

]
