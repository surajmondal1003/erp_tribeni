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
    CompanyProjectDetailsSerializer,
    CompanyProjectUpdateStatusSerializer,
    CompanyProjectReadSerializer

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

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = CompanyProjectReadSerializer(queryset, many=True)
    #     return Response(serializer.data)
    # def retrieve(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = CompanyProjectReadSerializer(queryset, many=True)
    #     return Response(serializer.data)




class SpecificCompanyProject(ListAPIView):

    serializer_class = CompanyProjectSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('project_name','project_address','project_state__state_name','project_city','project_contact_no')

    def get_queryset(self):
        company=self.kwargs['company']
        return CompanyProject.objects.filter(company_id=company,is_deleted=False).order_by('-id')




class SpecificCompanyProjectDropdown(ListAPIView):

    serializer_class = CompanyProjectSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        company=self.kwargs['company']
        return CompanyProject.objects.filter(company_id=company,status=True,is_deleted=False).order_by('-id')


class ProjectUpdateStatus(RetrieveUpdateAPIView):
    queryset = CompanyProject.objects.all()
    serializer_class = CompanyProjectUpdateStatusSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class AllCompanyProjectDropdown(ListAPIView):

    serializer_class = CompanyProjectSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return CompanyProject.objects.filter(status=True,is_deleted=False).order_by('-id')