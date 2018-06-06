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


from material_master.serializers import (
    MaterialTypeSerializer,
    MaterialSerializer,
    MaterialReadSerializer,
    MaterialUOMSerializerforRead


)
from django.contrib.auth.models import User
from material_master.models import MaterialType,Material,Material_Tax,Material_UOM

from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
class MaterialTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class =MaterialTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination


class MaterialTypeViewDropdown(ListAPIView):
    queryset = MaterialType.objects.filter(is_deleted=False)
    serializer_class =MaterialTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]






class MaterialReadView(ListAPIView):
    queryset = Material.objects.filter(is_deleted=False)
    serializer_class = MaterialReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('material_fullname','material_uom__base_uom__name','material_uom__unit_uom__name','material_tax__igst',
                     'material_tax__cgst','material_tax__sgst','material_tax__hsn')

    def get_queryset(self):

        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = Material.objects.filter(is_deleted=False).order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = Material.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = Material.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise



class MaterialMatser(ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]



class MaterialMatserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class MaterialReadDetailView(RetrieveAPIView):
    serializer_class = MaterialReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Material.objects.filter(material_uom__is_deleted=False,material_tax__is_deleted=False)


    def retrieve(self, request, *args, **kwargs):
        vendor_id = self.kwargs['pk']
        #queryset = Vendor.objects.filter(id=vendor_id, vendor_address__is_deleted=False)
        queryset = Material.objects.filter(material_uom__is_deleted=False, material_tax__is_deleted=False)

        serializer = MaterialReadSerializer(queryset,many=True)
        #print(queryset.query)
        return Response(serializer.data[0])




