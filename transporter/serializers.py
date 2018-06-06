from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from states.models import State
from django.contrib.auth.models import User
from company.models import Company
from transporter.models import Transport





class TransportSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    pan=serializers.CharField(required=False,allow_blank=True,allow_null=True)
    gstin=serializers.CharField(required=False,allow_blank=True,allow_null=True)
    email=serializers.EmailField(required=False,allow_blank=True,allow_null=True)

    class Meta:
        model = Transport
        fields = ['id','company','transporter_name','email','phone','state','city','pin','pan','gstin','status','created_at',
                  'created_by','is_deleted']