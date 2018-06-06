
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from company.serializers import CompanyListSerializer
from banks.models import Bank


class BankSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = Bank
        fields = ['id','company','bank_name','bank_branch','bank_ifsc','status','created_at','created_by','is_deleted']


class BankReadSerializer(ModelSerializer):

    company = CompanyListSerializer()
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = Bank
        fields = ['id','company','bank_name','bank_branch','bank_ifsc','status','created_at','created_by','is_deleted']