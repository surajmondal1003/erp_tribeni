from grn import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path



urlpatterns = [
    path('all_grn/',views.GRNReadViewList.as_view()),
    path('all_grn/<pk>/',views.GRNReadViewDetail.as_view()),
    path('grn/', views.GRNCreate.as_view()),
    path('grn/<pk>/', views.GRNUpdate.as_view()),
    path('grn_status/<pk>/', views.GRNUpdateStatus.as_view()),
    path('grn_dropdown/', views.GRNReadViewDropdown.as_view()),
    path('purchase_order_grn/<po_order>/', views.GRNByPurchaseOrder.as_view()),
    path('grn_search/', views.GRNSearchView.as_view()),


]
