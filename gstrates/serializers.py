from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from gstrates.models import GSTrates
from django.contrib.auth.models import User



class GSTSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = GSTrates
        fields = ['id','gst_pattern','igst','cgst','sgst','status','created_at','created_by','is_deleted']

