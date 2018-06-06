from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,GenericAPIView,RetrieveAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination

from uom.serializers import (
    UOMSerializer,

)
from django.contrib.auth.models import User
from company.models import Company
from uom.models import UOM
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import filters
from rest_framework import filters




class UOMViewSet(viewsets.ModelViewSet):
    queryset = UOM.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =UOMSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination

class UOMViewDropdown(ListAPIView):
    queryset = UOM.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = UOMSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
