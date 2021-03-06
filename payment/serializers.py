from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from uom.serializers import UOMSerializer
import datetime

from payment.models import Payment
from django.contrib.auth.models import User
from grn.serializers import GRNDetailReadSerializer,GRNReadSerializer,GRNCreateBySerializer
from company.serializers import CompanyListSerializer
from vendor.serializers import VendorAddressSerializer,VendorNameSerializer
from authentication.serializers import UserReadSerializer
from banks.serializers import BankSerializer
from company_project.serializers import CompanyProjectReadSerializer



class PaymentSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    is_paid = serializers.BooleanField(default=False)
    special_note=serializers.CharField(required=False)




    class Meta:
        model = Payment
        fields = ['id','pur_inv','bank','payment_mode',
                  'payment_refrence','total_amount','special_note','is_approve','is_paid','status','created_at',
                  'created_by','is_deleted']

    def create(self, validated_data):



        payment = Payment.objects.create(**validated_data)

        payment_no = str(datetime.date.today()) + '/PAY-00' + str(payment.id)

        payment.payment_no=payment_no
        payment.save()


        return payment

    def update(self, instance, validated_data):

            instance.bank = validated_data.get('bank', instance.bank)
            instance.payment_mode = validated_data.get('payment_mode', instance.payment_mode)
            instance.payment_refrence = validated_data.get('payment_refrence', instance.payment_refrence)
            instance.total_amount = validated_data.get('total_amount', instance.total_amount)
            instance.special_note = validated_data.get('special_note', instance.special_note)
            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_paid = validated_data.get('is_paid', instance.is_paid)
            instance.status = validated_data.get('status', instance.status)
            instance.created_at = validated_data.get('created_at', instance.created_at)
            instance.created_by = validated_data.get('created_by', instance.created_by)
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.save()

            return instance


class PaymentReadSerializer(ModelSerializer):

    created_by = UserReadSerializer()
    bank=BankSerializer()

    class Meta:
        model = Payment
        fields = ['id','pur_inv','bank','payment_mode',
                  'payment_refrence','total_amount','special_note','is_approve','is_paid','status','created_at',
                  'created_by','is_deleted','payment_no','company','pur_inv_no','po_order_no','vendor_name','project_name']




class PaymentUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id','status','is_approve','is_paid','is_deleted']


    def update(self, instance, validated_data):
            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.status = validated_data.get('status', instance.status)
            instance.is_paid = validated_data.get('is_paid', instance.is_paid)
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.save()

            return instance


class PaymentDropdownSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id','payment_no']