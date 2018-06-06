from states import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


router = routers.DefaultRouter()
router.register(r'states', views.StateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('active_states/',views.ActiveStateView.as_view()),


]
