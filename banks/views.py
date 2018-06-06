from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,RetrieveAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination
from django_filters.rest_framework import filters
from rest_framework import filters


from banks.serializers import (
    BankSerializer,
    BankReadSerializer,


)
from django.contrib.auth.models import User
from banks.models import Bank

from django_filters.rest_framework import DjangoFilterBackend

class BankReadView(ListAPIView):
    queryset = Bank.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = BankReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('bank_name','company__company_name','bank_branch','bank_ifsc','status','created_at')

    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = Bank.objects.filter(is_deleted=False).order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = Bank.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = Bank.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise



class BankReadDetailView(RetrieveAPIView):
    queryset = Bank.objects.filter(is_deleted=False)
    serializer_class = BankReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =BankSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('bank_name',)







class SpecificCompanyBankDropdown(ListAPIView):
    serializer_class =BankSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        company=self.kwargs['company']
        return Bank.objects.filter(company_id=company,status=True,is_deleted=False).order_by('-id')
