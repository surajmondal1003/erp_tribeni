from purchase_invoice import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path



urlpatterns = [
    path('all_purchase_invoice/',views.PurchaseInvoiceReadView.as_view()),
    path('all_purchase_invoice/<pk>/',views.PurchaseInvoiceReadDetailView.as_view()),
    path('purchase_invoice/', views.PurchaseInvoiceMatser.as_view()),
    path('purchase_invoice/<pk>/', views.PurchaseInvoiceUpdate.as_view()),
    path('purchase_invoice_status/<pk>/', views.PurchaseInvoiceUpdateStatus.as_view()),
    path('company_specific_invoice_dropdown/<company>/', views.CompanySpecificPurchaseInvoiceDropdown.as_view()),


]
