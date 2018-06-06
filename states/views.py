from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import viewsets, status
from states.models import State
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination, ErpPageNumberPagination
from django_filters.rest_framework import filters
from rest_framework import filters


from states.serializers import (
    StateSerializer,

)

from django_filters.rest_framework import DjangoFilterBackend



# Create your views here.
class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.filter(is_deleted=False).order_by('-id')
    serializer_class =StateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('state_name','tin_number','state_code')

    def get_queryset(self):

        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = State.objects.filter(is_deleted=False).order_by('-'+field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = State.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = State.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise



class ActiveStateView(ListAPIView):
    queryset = State.objects.filter(status=True,is_deleted=False).order_by('state_name')
    serializer_class =StateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
