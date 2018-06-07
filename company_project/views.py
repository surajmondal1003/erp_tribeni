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

from company_project.serializers import (
    CompanyProjectSerializer,
    CompanyProjectDetailsSerializer

)
from django.contrib.auth.models import User
from company.models import Company
from company_project.models import CompanyProjectDetail,CompanyProject
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import filters
from rest_framework import filters


# Create your views here.
class CompanyProjectViewSet(viewsets.ModelViewSet):
    queryset = CompanyProject.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =CompanyProjectSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('project_name','description','project_address','project_state','project_city','project_pincode',
                  'project_contact_no','contact_person','project_gstin','engineer_name','engineer_contact_no')
    def get_queryset(self):

        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = CompanyProject.objects.filter(is_deleted=False).order_by('-'+field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = CompanyProject.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = CompanyProject.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise




class SpecificCompanyBranchView(ListAPIView):

    serializer_class = CompanyBranchSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('branch_name','branch_address','branch_email','branch_gstin','branch_pan','branch_cin','branch_contact_no')

    def get_queryset(self):
        company=self.kwargs['company']
        return CompanyBranch.objects.filter(company_id=company,is_deleted=False).order_by('-id')



class CompanyStorageViewSet(viewsets.ModelViewSet):
    queryset = StorageLocation.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =CompanyStorageSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination



class SpecificCompanyStorageView(ListAPIView):

    serializer_class = CompanyStorageSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('storage_address', 'storage_contact_no', 'storage_email')

    def get_queryset(self):
        company=self.kwargs['company']
        return StorageLocation.objects.filter(company_id=company,is_deleted=False).order_by('-id')



class UOMViewSet(viewsets.ModelViewSet):
    queryset = UOM.objects.all().order_by('-id')
    serializer_class =UOMSerializer
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination

class CompanyStorageBinViewSet(viewsets.ModelViewSet):
    queryset = StorageBin.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =CompanyStorageBinSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination



class SpecificCompanyStorageBinView(ListAPIView):

    serializer_class = CompanyStorageBinReadSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('bin_no', 'bin_volume', 'uom__name')

    def get_queryset(self):
        company=self.kwargs['company']
        return StorageBin.objects.filter(company_id=company,is_deleted=False).order_by('-id')




class SpecificCompanyBranchDropdown(ListAPIView):

    serializer_class = CompanyBranchSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        company=self.kwargs['company']
        return CompanyBranch.objects.filter(company_id=company,status=True,is_deleted=False).order_by('-id')



class SpecificCompanyStorageDropdown(ListAPIView):

    serializer_class = CompanyStorageSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        company=self.kwargs['company']
        return StorageLocation.objects.filter(company_id=company,status=True,is_deleted=False).order_by('-id')


class SpecificCompanyStorageBinDropdown(ListAPIView):

    serializer_class = CompanyStorageBinSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        company=self.kwargs['company']
        return StorageBin.objects.filter(company_id=company,status=True,is_deleted=False).order_by('-id')

