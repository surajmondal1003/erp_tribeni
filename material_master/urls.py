from material_master import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'all_material_type', views.MaterialTypeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('all_material_master/',views.MaterialReadView.as_view()),
    path('material_master/', views.MaterialMatser.as_view()),
    path('material_master/<pk>/', views.MaterialMatserUpdate.as_view()),
    path('all_material_master/<pk>/', views.MaterialReadDetailView.as_view()),
    path('all_material_type_dropdown/', views.MaterialTypeViewDropdown.as_view()),
    path('specific_project_material/<project_id>/<mtype_id>/', views.ProjectSpecificMaterialList.as_view()),
    path('specific_project_materialtype/<project_id>/', views.ProjectSpecificMaterialTypeList.as_view()),

]
