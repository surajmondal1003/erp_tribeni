from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination
from django_filters.rest_framework import filters
from rest_framework import filters

from contractor.serializers import (
    ContractorAccountSerializer,
    ContractorSerializer,
    ContractorUpdateStatusSerializer

)
from django.contrib.auth.models import User
from contractor.models import ContractorAccount,Contractor

from django_filters.rest_framework import DjangoFilterBackend



class ContractorMatserCreate(ListCreateAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination



class ContractorMatserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class ContractorReadView(ListAPIView):
    queryset = Contractor.objects.filter(is_deleted=False)
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('contractor_name',)
    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = Contractor.objects.filter(is_deleted=False).order_by('-'+field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = Contractor.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = Contractor.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise



class ContractorReadDropdown(ListAPIView):
    queryset = Contractor.objects.filter(status=True,is_deleted=False)
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ContractorMatserStatusUpdate(RetrieveUpdateAPIView):
    queryset = Contractor.objects.all()
    serializer_class = ContractorUpdateStatusSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
