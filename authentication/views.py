from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets,status

from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from authentication.pagination import ErpLimitOffestpagination,ErpPageNumberPagination


from authentication.serializers import (
    UserLoginSerializer,

   )

# Create your views here.

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

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username':user.username,
                'email': user.email,
                'user_type':user_group
            })
        else:
            return Response({'message':'Invalid Login','status':status.HTTP_400_BAD_REQUEST})

