from company_branch.models import CompanyBranch,StorageLocation,UOM,StorageBin
from states.models import State
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

class CompanyBranchSerializer(ModelSerializer):
    branch_name = serializers.CharField(
        validators=[UniqueValidator(queryset=CompanyBranch.objects.all())]
    )

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.BooleanField(default=True)

    class Meta:
        model = CompanyBranch
        fields = ['id','company','branch_name','branch_address','branch_state','branch_city','branch_pincode','branch_contact_no',
                  'branch_email','branch_gstin','branch_pan','branch_cin','status','created_at','created_by','is_deleted']


class CompanyStorageSerializer(ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.BooleanField(default=True)

    class Meta:
        model = StorageLocation
        fields = ['id','company','branch','storage_address','storage_state','storage_city','storage_pincode','storage_contact_no',
                  'storage_email','status','created_at','created_by','is_deleted']


class UOMSerializer(ModelSerializer):

    class Meta:
        model = UOM
        fields = ['id','name']





class CompanyStorageBinReadSerializer(ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.BooleanField(default=True)
    uom=UOMSerializer()

    class Meta:
        model = StorageBin
        fields = ['id','company','branch','storage','uom','bin_no','bin_volume','status','created_at','created_by','is_deleted']


class CompanyStorageBinSerializer(ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.BooleanField(default=True)

    class Meta:
        model = StorageBin
        fields = ['id','company','branch','storage','uom','bin_no','bin_volume','status','created_at','created_by','is_deleted']
