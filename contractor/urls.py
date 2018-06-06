from contractor import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path



urlpatterns = [

    path('contractor_master/', views.ContractorMatserCreate.as_view()),
    path('contractor_master/<pk>/', views.ContractorMatserUpdate.as_view()),
    path('contractor_master_status/<pk>/', views.ContractorMatserStatusUpdate.as_view()),
    path('contractor_dropdown/', views.ContractorReadDropdown.as_view()),
    path('all_contractor/', views.ContractorReadView.as_view()),


]