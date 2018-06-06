from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination
from django_filters.rest_framework import filters
from rest_framework import filters


from gstrates.serializers import (
    GSTSerializer,



)
from django.contrib.auth.models import User
from gstrates.models import GSTrates

from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
class GSTViewSet(viewsets.ModelViewSet):
    queryset = GSTrates.objects.filter(is_deleted=False)
    serializer_class =GSTSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('gst_pattern','igst','cgst','sgst')

    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = GSTrates.objects.filter(is_deleted=False).order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = GSTrates.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = GSTrates.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise


# Create your views here.
class GSTDropdown(ListAPIView):
    queryset = GSTrates.objects.filter(status=True,is_deleted=False)
    serializer_class =GSTSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

