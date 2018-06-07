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
from datetime import datetime,timedelta,time,date
from django.utils import timezone


from grn.serializers import (
    GRNSerializer,
    GRNDetailSerializer,
    GRNReadSerializer,
    GRNUpdateStatusSerializer,
    ReversGRNSerializer

)
from django.contrib.auth.models import User
from grn.models import ReversGRN,GRNDetail,GRN

from django_filters.rest_framework import DjangoFilterBackend



class GRNReadViewList(ListAPIView):
    queryset = GRN.objects.filter(is_deleted=False)
    serializer_class = GRNReadSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('grn_map__grn_no','company__company_name','pur_org__name','pur_grp__name','vendor__vendor_fullname',
                     'vendor_address__address','po_order__purchase_order_map__purchase_order_no')


    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = GRN.objects.filter(is_deleted=False).order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = GRN.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = GRN.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise




class GRNReadViewDropdown(ListAPIView):
    queryset = GRN.objects.filter(status=True, is_approve=1, is_finalised=0,is_deleted=False)
    serializer_class = GRNReadSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]




class GRNReadViewDetail(RetrieveAPIView):
    queryset = GRN.objects.all()
    serializer_class = GRNReadSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]



class GRNCreate(ListCreateAPIView):
    queryset = GRN.objects.all()
    serializer_class = GRNSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination


class ReversGRNCreate(ListCreateAPIView):
    queryset = ReversGRN.objects.all()
    serializer_class = ReversGRNSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination


class GRNUpdate(RetrieveUpdateDestroyAPIView):
    queryset = GRN.objects.all()
    serializer_class = GRNSerializer
    #permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]

class GRNByPurchaseOrder(ListAPIView):
    serializer_class = GRNReadSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        po_order=self.kwargs['po_order']
        return GRN.objects.filter(po_order_id=po_order,status=True,is_deleted=False)
    # def get_queryset(self):
    #     requisition=self.kwargs['requisition']
    #     return PurchaseOrder.objects.filter(requisition_id=requisition)


class GRNUpdateStatus(RetrieveUpdateAPIView):
    queryset = GRN.objects.all()
    serializer_class = GRNUpdateStatusSerializer


class GRNSearchView(ListAPIView):

    serializer_class = GRNReadSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination

    def get_queryset(self):
        queryset = GRN.objects.all()

        company = self.request.query_params.get('company', None)
        status = self.request.query_params.get('status', None)
        approve=self.request.query_params.get('approve', None)
        from_date=self.request.query_params.get('from_date', None)
        to_date=self.request.query_params.get('to_date', None)
        created_at=self.request.query_params.get('created_at', None)
        vendor = self.request.query_params.get('vendor', None)

        if company is not None:
            queryset = queryset.filter(company_id=company)

        if status is not None:
            queryset = queryset.filter(status=status)

        if approve is not None:
            queryset = queryset.filter(is_approve=approve)

        if vendor is not None:
            queryset = queryset.filter(vendor_id=vendor)

        if created_at is not None:

            created_from_date = datetime.strptime(created_at, "%Y-%m-%d").date()
            created_from_date = datetime.combine(created_from_date, time.min)
            created_from_date = datetime.isoformat(created_from_date)

            created_to_date = datetime.strptime(created_at, "%Y-%m-%d").date()
            created_to_date = datetime.combine(created_to_date, time.max)
            created_to_date = datetime.isoformat(created_to_date)

            queryset = queryset.filter(created_at__gte=created_from_date,created_at__lte=created_to_date)


        if from_date and to_date is not None:

            created_from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
            created_from_date = datetime.combine(created_from_date, time.min)
            created_from_date = datetime.isoformat(created_from_date)

            created_to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            created_to_date = datetime.combine(created_to_date, time.max)
            created_to_date = datetime.isoformat(created_to_date)

            queryset = queryset.filter(created_at__gte=created_from_date,created_at__lte=created_to_date)

        return queryset

