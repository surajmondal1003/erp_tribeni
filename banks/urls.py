from banks import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'banks', views.BankViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('all_bank/',views.BankReadView.as_view()),
    path('all_bank/<pk>/',views.BankReadDetailView.as_view()),
    path('company_specific_bank_dropdown/<company>/',views.SpecificCompanyBankDropdown.as_view()),


]
