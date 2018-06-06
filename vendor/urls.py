from vendor import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'all_vendor_type', views.VendorTypeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('vendor_master/', views.VendorMatserCreate.as_view()),
    path('vendor_master/<pk>/', views.VendorMatserUpdate.as_view()),
    path('vendor_master_status/<pk>/', views.VendorMatserStatusUpdate.as_view()),
    path('vendor_dropdown/', views.VendorReadDropdown.as_view()),
    path('all_vendor/', views.VendorReadView.as_view()),
    path('all_vendor/<pk>/', views.VendorReadDetailView.as_view()),


]