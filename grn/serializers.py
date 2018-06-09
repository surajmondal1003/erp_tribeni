from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
import datetime

from grn.models import GRN,GRNDetail,ReversGRN
from django.contrib.auth.models import User
from vendor.serializers import VendorAddressSerializer
from uom.serializers import UOMSerializer
from purchase_order.serializers import (
    PurchaseOrderSerializer,
    PurchaseDetailSerializer,
    PurchaseOrderReadSerializer,
    PurchaseOrderReadForGRNSerializer
)


from rest_framework.relations import StringRelatedField
from material_master.serializers import MaterialNameSerializer
from vendor.serializers import VendorNameSerializer

from company.serializers import CompanyListSerializer
from company_project.serializers import CompanyProjectSerializer,CompanyProjectDetailsSerializer,CompanyProjectUpdateStatusSerializer
from authentication.serializers import UserReadSerializer
from purchase_requisition.serializers import RequisitionProjectNameSerializer





class GRNDetailSerializer(ModelSerializer):

    class Meta:
        model = GRNDetail
        fields = ['id','material','order_quantity','receive_quantity']


class GRNSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    grn_detail = GRNDetailSerializer(many=True)


    class Meta:
        model = GRN
        fields = ['id','po_order','company','vendor','vendor_address','waybill_no','vehicle_no',
                  'check_post','challan_no','challan_date','is_approve','is_finalised','status','created_at',
                  'created_by','grn_detail','is_deleted']



    def create(self, validated_data):

        grn_detail_data = validated_data.pop('grn_detail')

        grn = GRN.objects.create(**validated_data)

        grn_no = str(datetime.date.today()) + '/GRN-00' + str(grn.id)

        for grn_detail in grn_detail_data:
            GRNDetail.objects.create(grn=grn, **grn_detail)


        grn.grn_no = grn_no
        grn.save()


        return grn

    def update(self, instance, validated_data):

            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)

            instance.save()

            return instance




class GRNDetailReadSerializer(ModelSerializer):
    material = MaterialNameSerializer(read_only=True)
    company_project = CompanyProjectSerializer(read_only=True)

    class Meta:
        model = GRNDetail
        fields = ['id','material','material_uom','order_quantity','receive_quantity','company_project','material_uom']



class GRNProjectReadSerializer(ModelSerializer):


    class Meta:
        model = GRN
        fields = ['project_id','project_name']


class GRNReadSerializer(ModelSerializer):

    po_order=PurchaseOrderReadForGRNSerializer(read_only=True)
    company=CompanyListSerializer()
    vendor=VendorNameSerializer(read_only=True)
    vendor_address=VendorAddressSerializer()
    grn_detail = GRNDetailReadSerializer(many=True)
    created_by = UserReadSerializer()
    #project = GRNProjectReadSerializer()


    class Meta:
        model = GRN
        fields = ['id','grn_no','po_order','company','vendor','vendor_address','waybill_no','vehicle_no',
                  'check_post','challan_no','challan_date','is_approve','is_finalised','status','created_at',
                  'created_by','grn_detail','is_deleted','purchase_order_no']


class GRNCreateBySerializer(ModelSerializer):
    created_by = UserReadSerializer()

    class Meta:
        model = GRN
        fields = ['id','created_at','created_by']




class GRNUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = GRN
        fields = ['id','status','is_approve','is_finalised','is_deleted']


    def update(self, instance, validated_data):
            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.save()

            return instance




class ReversGRNSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)


    class Meta:
        model = ReversGRN
        fields = ['id','grn','reverse_quantity','created_at','created_by','reverse_reason','status','is_approve','is_finalised']


    def create(self, validated_data):

        grn_data = validated_data.pop('grn')

        revers_grn = ReversGRN.objects.create(**validated_data)

        revers_gen_no = str(datetime.date.today()) + '/REGRN-00' + str(revers_grn.id)

        revers_grn.revers_gen_no = revers_gen_no
        revers_grn.save()
        return revers_gen_no

    def update(self, instance, validated_data):

            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)

            instance.save()

            return instance

class ReversGRNReadSerializer(ModelSerializer):
    # grn = GRNReadSerializer(many=True)
    created_by = UserReadSerializer()
    class Meta:
        model = ReversGRN
        fields = ['id', 'grn','revers_gen_no','reverse_quantity','created_at','created_by','reverse_reason','status','is_approve',
                  'is_finalised']



