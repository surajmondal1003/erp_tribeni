from designation import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('all_designation/',views.DesignationReadView.as_view()),
    path('all_designation/<pk>/', views.DesignationReadDetailView.as_view()),
    path('designation/', views.DesignationMatser.as_view()),
    path('designation/<pk>/', views.DesignationUpdate.as_view()),
    path('designation_dropdown/<department>/', views.SpecificDepartmentDesignationDropdown.as_view()),
    path('designation_status/<pk>/', views.DesignationUpdateStatus.as_view()),
]