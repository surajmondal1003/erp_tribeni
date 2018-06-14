from stock import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


urlpatterns = [
    path('all_stock/',views.StockViewReadView.as_view()),
    path('all_stock/<pk>/', views.StocktReadDetailView.as_view()),
    path('all_stock_issue/',views.StockIssueReadView.as_view()),
    path('stock/', views.StockMatser.as_view()),
    path('stock/<pk>/', views.StockUpdate.as_view()),
    path('stock_issue/',views.StockIssueCreate.as_view()),
    path('specific_stock_issue/<stock>/',views.SpecificStockIssueView.as_view())

]
