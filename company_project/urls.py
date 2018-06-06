from company_branch import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'all_branch', views.CompanyBranchViewSet)
router.register(r'all_storage', views.CompanyStorageViewSet)
router.register(r'uom', views.UOMViewSet)
router.register(r'all_storage_bin', views.CompanyStorageBinViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('company_branch/<company>/',views.SpecificCompanyBranchView.as_view()),
    path('company_storage/<company>/',views.SpecificCompanyStorageView.as_view()),
    path('company_storagebin/<company>/',views.SpecificCompanyStorageBinView.as_view()),
    path('company_branch_dropdown/<company>/',views.SpecificCompanyBranchDropdown.as_view()),
    path('company_storage_dropdown/<company>/',views.SpecificCompanyStorageDropdown.as_view()),
    path('company_storagebin_dropdown/<company>/',views.SpecificCompanyStorageBinDropdown.as_view()),

]

