from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListCreateAPIView,ListAPIView,RetrieveAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination,ErpPageNumberPagination
from appapprovepermission.models import AppApprove,EmpApprove
from django.contrib.contenttypes.models import ContentType
from appapprovepermission.serializers import (
    AppApproveSerializer,
    EmpApproveSerializer,
    ContentDropdownSerializer,
    EmpApproveReadSerializer
   )
from django_filters.rest_framework import filters
from rest_framework import filters
from django.contrib.auth.models import Permission
from attendance.models import Attendance
import calendar
from datetime import datetime,timedelta,time,date

# Create your views here.dat


class AppApproveView(ListAPIView):
    """
    Creates the user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AppApproveSerializer
    queryset = AppApprove.objects.all()



class EmpAppApproveView(ListCreateAPIView):
    """
    Creates the user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = EmpApproveSerializer
    queryset = EmpApprove.objects.all()



class EmpAppApproveReadView(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = EmpApproveReadSerializer
    queryset = EmpApprove.objects.all()
    pagination_class = ErpPageNumberPagination

class EmpAppDetailApproveReadView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = EmpApproveSerializer
    queryset = EmpApprove.objects.all()


class EmpAppApproveUpadteView(RetrieveUpdateDestroyAPIView):
    """
    Creates the user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = EmpApproveSerializer
    queryset = EmpApprove.objects.all()


class ContentDropdown(ListAPIView):
    """
    Creates the user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ContentDropdownSerializer
    queryset = ContentType.objects.all()