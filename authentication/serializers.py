from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',

        ]


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',


        ]

