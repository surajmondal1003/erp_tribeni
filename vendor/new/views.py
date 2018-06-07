from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination
from django_filters.rest_framework import filters
from rest_framework import filters
from django.db.models import Q


from vendor.serializers import (
    VendorTypeSerializer,
    VendorAccountSerializer,
    VendorAddressSerializer,
    VendorSerializer,
    VendorUpdateStatusSerializer,
    VendorReadSerializer



)
from django.contrib.auth.models import User
from vendor.models import VendorType,VendorAccount,VendorAddress,Vendor

from django_filters.rest_framework import DjangoFilterBackend



class VendorTypeViewSet(viewsets.ModelViewSet):
    queryset = VendorType.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =VendorTypeSerializer
    #permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('vendor_type',)

    def get_queryset(self):

        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = VendorType.objects.filter(is_deleted=False).order_by('-'+field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = VendorType.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = VendorType.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise



class VendorReadView(ListAPIView):
    queryset = Vendor.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = VendorSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('vendor_fullname','pan_no','gst_no','cin_no','vendor_address__mobile')

    def get_queryset(self):

        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = Vendor.objects.filter(is_deleted=False).order_by('-'+field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = Vendor.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = Vendor.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise


class VendorReadDropdown(ListAPIView):
    queryset = Vendor.objects.filter(status=True,is_deleted=False)
    serializer_class = VendorSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]



class VendorMatserCreate(ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination



class VendorMatserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]



class VendorMatserStatusUpdate(RetrieveUpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorUpdateStatusSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]


class VendorReadDetailView(RetrieveAPIView):
    serializer_class = VendorReadSerializer
    # permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]
    queryset = Vendor.objects.filter(vendor_address__is_deleted=False,vendor_account__is_deleted=False)


    def retrieve(self, request, *args, **kwargs):
        vendor_id = self.kwargs['pk']
        #queryset = Vendor.objects.filter(id=vendor_id, vendor_address__is_deleted=False)
        queryset = Vendor.objects.filter(id=vendor_id, vendor_address__is_deleted=False,vendor_account__is_deleted=False)
        serializer = VendorReadSerializer(queryset,many=True)
        #print(queryset.query)
        return Response(serializer.data[0])

