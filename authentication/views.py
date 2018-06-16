from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListCreateAPIView,ListAPIView,RetrieveAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import viewsets,status

from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination,ErpPageNumberPagination
from authentication.models import EmployeeProfile


from authentication.serializers import (
    UserLoginSerializer,
    UserSerializer,
    EmployeeReadSerializer,
    EmployeeProfileSerializer

   )
from django_filters.rest_framework import filters
from rest_framework import filters
from django.contrib.auth.models import Permission

# Create your views here.dat

class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response=super(CustomObtainAuthToken,self).post(request,*args,**kwargs)
        token=Token.objects.get(key=response.data['token'])
        user=User.objects.get(id=token.user_id)
        serializer=UserLoginSerializer(user,many=True)

        if user:
            #user_groups=list()
            user_group=user.groups.all()
            for item in user_group:
                user_group=item.name
            perm_tuple = [{'id':x.id, 'name':x.name} for x in Permission.objects.filter(user=user)]

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username':user.username,
                'email': user.email,
                'user_type':user_group,
                'group_permissions':user.get_group_permissions(),
                'user_permissions':perm_tuple,

            })
        else:
            return Response({'message':'Invalid Login','status':status.HTTP_400_BAD_REQUEST})


class UserCreate(ListCreateAPIView):
    """
    Creates the user.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer

    # def post(self, request, format='json'):
    #     user_serializer = UserSerializer(data=request.data)
    #     if user_serializer.is_valid():
    #         user=user_serializer.save()
    #         if user:
    #             serializer = UserSerializer(instance=user)
    #             return Response({'username':user.username,'message':'success'},status=status.HTTP_201_CREATED)
    #     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeReadView(ListAPIView):
    queryset = EmployeeProfile.objects.filter(is_deleted=False)
    serializer_class = EmployeeReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = ErpPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name','last_name','email','contact','company__company_name','departments__department_name',
                     'designation__designation_name','status')

    def get_queryset(self):
        try:
            order_by = self.request.query_params.get('order_by', None)
            field_name = self.request.query_params.get('field_name', None)

            if order_by and order_by.lower() == 'desc' and field_name:
                queryset = EmployeeProfile.objects.filter(is_deleted=False).order_by('-' + field_name)
            elif order_by and order_by.lower() == 'asc' and field_name:
                queryset = EmployeeProfile.objects.filter(is_deleted=False).order_by(field_name)
            else:
                queryset = EmployeeProfile.objects.filter(is_deleted=False).order_by('-id')
            return queryset

        except Exception as e:
            raise

class EmployeeReadDetailView(RetrieveAPIView):
    queryset = EmployeeProfile.objects.filter(is_deleted=False)
    serializer_class = EmployeeReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class EmployeeMatserUpdate(RetrieveUpdateDestroyAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class EmployeeDropdwon(ListAPIView):
    queryset = EmployeeProfile.objects.filter(is_deleted=False)
    serializer_class = EmployeeReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
