from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView,ListCreateAPIView,RetrieveAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination
from django_filters.rest_framework import filters
from rest_framework import filters

from designation.serializers import (
    DesignationSerializer,
    DesignationReadSerializer,
    DesignationListSerializer,
    DesignationUpdateStatusSerializer

)

from django.contrib.auth.models import User
from designation.models import Designation

# Create your views here.


class DesignationReadView(ListAPIView):
    queryset = Designation.objects.filter(is_deleted=False)
    serializer_class =DesignationReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('designation_name','departments__department_name','company__company_name')

    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = Designation.objects.filter(is_deleted=False).order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = Designation.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = Designation.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise


class DesignationReadDetailView(RetrieveAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class DesignationMatser(ListCreateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    authentication_classes = [TokenAuthentication]


class DesignationUpdate(RetrieveUpdateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class SpecificDepartmentDesignationDropdown(ListAPIView):

    serializer_class = DesignationListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        department=self.kwargs['department']
        return Designation.objects.filter(departments=department,is_deleted=False)



class DesignationUpdateStatus(RetrieveUpdateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationUpdateStatusSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]