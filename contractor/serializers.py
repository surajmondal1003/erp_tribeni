from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from contractor.models import Contractor,ContractorAccount







class ContractorAccountSerializer(ModelSerializer):
    class Meta:
        model = ContractorAccount
        fields = ['id', 'bank_name', 'branch_name', 'account_no', 'ifsc_code']



class ContractorSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    contractor_account = ContractorAccountSerializer(many=True)


    class Meta:
        model = Contractor
        fields = ['id','contractor_name','pan_no','gst_no','address','state','city','pincode','mobile','email','status','created_at','created_by',
                  'is_deleted','contractor_account']

    def create(self, validated_data):

            contractor_account_data = validated_data.pop('contractor_account')

            contractor = Contractor.objects.create(**validated_data)

            for contractor_account in contractor_account_data:
                ContractorAccount.objects.create(contractor=contractor, **contractor_account)

            return contractor

    def update(self, instance, validated_data):

            contractor_account_data = validated_data.pop('contractor_account')

            contractor_accounts = (instance.contractor_account).all()
            contractor_accounts = list(contractor_accounts)


            instance.contractor_name = validated_data.get('contractor_name', instance.contractor_name)
            instance.pan_no = validated_data.get('pan_no', instance.pan_no)
            instance.gst_no = validated_data.get('gst_no', instance.gst_no)
            instance.address = validated_data.get('address', instance.address)
            instance.state = validated_data.get('state', instance.state)
            instance.city = validated_data.get('city', instance.city)
            instance.pincode = validated_data.get('pincode', instance.pincode)
            instance.mobile = validated_data.get('mobile', instance.mobile)
            instance.email = validated_data.get('email', instance.email)
            instance.status = validated_data.get('status', instance.status)
            instance.created_at = validated_data.get('created_at', instance.created_at)
            instance.created_by = validated_data.get('created_by', instance.created_by)
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.save()

            print(instance)


            for contractor_account in contractor_accounts:
                if contractor_account:
                    contractor_account.delete()


            for contractor_account in contractor_account_data:
                ContractorAccount.objects.create(contractor=instance, **contractor_account)


            return instance



class ContractorUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = Contractor
        fields = ['id','status','is_deleted']


    def update(self, instance, validated_data):
            instance.status = validated_data.get('status', instance.status)
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.save()

            return instance