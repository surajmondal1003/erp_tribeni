from gstrates import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'gst_rates', views.GSTViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('gst_rates_dropdown/',views.GSTDropdown.as_view()),

]
