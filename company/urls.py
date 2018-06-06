from company import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from company.views import CompanyListView, PurchaseOrganisationSpecificCompanyList, TermsAndConditionsDropdown, TermsAndConditionsReadView

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'terms_conditions', views.TermsAndConditionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('company_dropdownlist/', CompanyListView.as_view(),name='company_list'),
    path('specific_organisation_company/<org_id>/', PurchaseOrganisationSpecificCompanyList.as_view()),
    path('terms_conditions_dropdown/', TermsAndConditionsDropdown.as_view()),
    path('all_terms_conditions/', TermsAndConditionsReadView.as_view()),
]
