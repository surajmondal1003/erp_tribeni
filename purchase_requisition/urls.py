from purchase_requisition import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path



urlpatterns = [
    path('all_purchase_requistion/',views.RequisitionReadView.as_view()),
    path('all_purchase_requistion/<pk>/',views.RequisitionReadDetailView.as_view()),
    path('purchase_requistion/', views.RequisitionMatser.as_view()),
    path('purchase_requistion/<pk>/', views.RequisitionUpdate.as_view()),
    path('purchase_requistion_status/<pk>/', views.RequisitionUpdateStatus.as_view()),
    path('purchase_requistion_dropdown/', views.RequisitionReadDropdown.as_view()),
    path('purchase_requistion_search/', views.RequisitioSearchView.as_view()),


]
