from company_project import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'all_company_project', views.CompanyProjectViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('company_project/<company>/',views.SpecificCompanyProject.as_view()),
    path('company_project_dropdown/<company>/',views.SpecificCompanyProjectDropdown.as_view()),
    path('all_company_project_dropdown/',views.AllCompanyProjectDropdown.as_view()),


]

