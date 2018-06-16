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
    AttendanceReadSerializer
   )
from django_filters.rest_framework import filters
from rest_framework import filters
from django.contrib.auth.models import Permission
from attendance.models import Attendance
import calendar
from datetime import datetime,timedelta,time,date

# Create your views here.dat


class AttendanceView(ListCreateAPIView):
    """
    Creates the user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.filter(is_deleted=False)

class AttendanceUpadteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.filter(is_deleted=False)


class SpecificEmployeeAttendanceView(ListCreateAPIView):
    """
    Creates the user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AttendanceReadSerializer

    def get_queryset(self):
        emp = self.kwargs['emp']
        month = self.request.query_params.get('month', None)
        queryset= Attendance.objects.filter(employee=emp, is_deleted=False).order_by('-id')
        if month  is not None:

            def get_first_day(dt, d_years=0, d_months=0):
                # d_years, d_months are "deltas" to apply to dt
                y, m = dt.year + d_years, dt.month + d_months
                a, m = divmod(m - 1, 12)
                return date(y + a, m + 1, 1)

            def get_last_day(dt):
                return get_first_day(dt, 0, 1) + timedelta(-1)

            d=datetime.strptime(month, "%Y-%m-%d").date()
            first_day=get_first_day(d)
            last_day=get_last_day(d)
            queryset = Attendance.objects.filter(employee=emp, is_deleted=False,date__gte=first_day,date__lte=last_day).order_by('-id')

        return queryset

