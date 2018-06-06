from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView,ListAPIView
from rest_framework import viewsets, status
from company.models import Company,TermsandConditon
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination

from company.serializers import (
    CompanySerializer,
    CompanyListSerializer,
    TermsAndConditionSerializer,
    TermsAndConditionReadSerializer

)

from django_filters.rest_framework import filters
from rest_framework import filters


# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(is_deleted=False)
    serializer_class =CompanySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = Company.objects.filter(parent=None)
        serializer = CompanySerializer(queryset,many=True)
        return Response(serializer.data)


class CompanyListView(ListAPIView):
    queryset = Company.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class TermsAndConditionsViewSet(viewsets.ModelViewSet):
    queryset = TermsandConditon.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =TermsAndConditionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('term_text','term_text','company__company_name')

    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = TermsandConditon.objects.filter(is_deleted=False).order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = TermsandConditon.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = TermsandConditon.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = TermsAndConditionReadSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)





class TermsAndConditionsDropdown(ListAPIView):
    queryset = TermsandConditon.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =TermsAndConditionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]





class PurchaseOrganisationSpecificCompanyList(ListAPIView):
    queryset = Company.objects.filter(is_deleted=False)
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = ('org_id')

    def get_queryset(self):
        org_id = self.kwargs['org_id']
        return Company.objects.filter(company_branch__purchaseorgmapping__pur_org_id=org_id,is_deleted=False)




class TermsAndConditionsReadView(ListAPIView):
    queryset = TermsandConditon.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = TermsAndConditionReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('term_text', 'term_text', 'company__company_name')
