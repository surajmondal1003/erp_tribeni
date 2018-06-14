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


from purchase_invoice.serializers import (
    PurchaseInvoiceSerializer,
    PurchaseInvoiceReadSerializer,
    InvoiceUpdateStatusSerializer


)
from django.contrib.auth.models import User
from purchase_invoice.models import PurchaseInvoice,PurchaseInvoiceDetail

from django_filters.rest_framework import DjangoFilterBackend




class PurchaseInvoiceReadView(ListAPIView):
    queryset = PurchaseInvoice.objects.all()
    serializer_class = PurchaseInvoiceReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('company__company_name','purchase_inv_no','grn__po_order__purchase_order_no','grn__grn_no',
                      'grn__po_order__requisition__project__project_name')

    def get_queryset(self):
        try:
            queryset = PurchaseInvoice.objects.all().order_by('-id')
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)
            project = self.request.query_params.get('project', None)
            company = self.request.query_params.get('company', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = PurchaseInvoice.objects.all().order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = PurchaseInvoice.objects.all().order_by(field_name)
            elif project is not None:
                queryset = queryset.filter(grn__po_order__requisition__project=project)
            elif company is not None:
                queryset = queryset.filter(company=company)
            else:
                queryset = PurchaseInvoice.objects.all().order_by('-id')
            return queryset

        except Exception as e:
            raise



class PurchaseInvoiceReadDetailView(RetrieveAPIView):
    queryset = PurchaseInvoice.objects.all()
    serializer_class = PurchaseInvoiceReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class PurchaseInvoiceMatser(ListCreateAPIView):
    queryset = PurchaseInvoice.objects.all()
    serializer_class = PurchaseInvoiceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]





class PurchaseInvoiceUpdate(RetrieveUpdateDestroyAPIView):
    queryset = PurchaseInvoice.objects.all()
    serializer_class = PurchaseInvoiceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class CompanySpecificPurchaseInvoiceDropdown(ListAPIView):
    queryset = PurchaseInvoice.objects.filter(status=True, is_approve=1, is_finalised=0)
    serializer_class = PurchaseInvoiceReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        company=self.kwargs['company']
        return PurchaseInvoice.objects.filter(company=company, status=True, is_approve=1 , is_finalised=0 )


class PurchaseInvoiceUpdateStatus(RetrieveUpdateAPIView):
    queryset = PurchaseInvoice.objects.all()
    serializer_class = InvoiceUpdateStatusSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]