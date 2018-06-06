from uom import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()

router.register(r'uom', views.UOMViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('uom_dropdown/', views.UOMViewDropdown.as_view()),

]

