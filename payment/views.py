from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,RetrieveAPIView,RetrieveUpdateAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination
from django_filters.rest_framework import filters
from rest_framework import filters


from payment.serializers import (
    PaymentSerializer,
    PaymentReadSerializer,
    PaymentUpdateStatusSerializer,
    PaymentDropdownSerializer

)
from django.contrib.auth.models import User
from payment.models import Payment
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime,timedelta,time,date




class PaymentReadView(ListAPIView):
    queryset = Payment.objects.filter(is_deleted=False)
    serializer_class = PaymentReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('company__company_name','vendor__vendor_fullname','payment_no')


    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = Payment.objects.filter().order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = Payment.objects.filter().order_by(field_name)
            else:
                queryset = Payment.objects.filter().order_by('-id')
            return queryset

        except Exception as e:
            raise



class PaymentReadDetailView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class PaymentMatser(ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class PaymentMatserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class PaymentUpdateStatus(RetrieveUpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentUpdateStatusSerializer


class PaymentDropdownView(ListAPIView):
    queryset = Payment.objects.filter(status=True,is_deleted=False)
    serializer_class = PaymentDropdownSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class PaymentSearchView(ListAPIView):

    serializer_class = PaymentReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination

    def get_queryset(self):
        queryset = Payment.objects.all()
        company = self.request.query_params.get('company', None)
        from_date=self.request.query_params.get('from_date', None)
        to_date=self.request.query_params.get('to_date', None)
        vendor = self.request.query_params.get('vendor', None)
        paid = self.request.query_params.get('paid', None)



        if company is not None:
            queryset = queryset.filter(company_id=company)

        if vendor is not None:
            queryset = queryset.filter(vendor_id=vendor)

        if paid is not None:
            queryset = queryset.filter(is_paid=paid)

        if from_date and to_date is not None:

            created_from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            created_from_date = datetime.combine(created_from_date, time.min)
            created_from_date = datetime.isoformat(created_from_date)

            created_to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            created_to_date = datetime.combine(created_to_date, time.max)
            created_to_date = datetime.isoformat(created_to_date)

            queryset = queryset.filter(created_at__gte=created_from_date,created_at__lte=created_to_date)

        return queryset