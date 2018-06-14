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
from authentication.models import EmployeeProfile
from attendance.serializers import (
    AttendanceSerializer,
   )
from django_filters.rest_framework import filters
from rest_framework import filters
from django.contrib.auth.models import Permission
from attendance.models import Attendance

# Create your views here.dat


class AttendanceView(ListCreateAPIView):
    """
    Creates the user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.filter(is_deleted=False)

