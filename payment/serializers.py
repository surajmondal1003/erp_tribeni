from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from company_branch.serializers import UOMSerializer
import datetime

from payment.models import Payment,PaymentMap
from django.contrib.auth.models import User
from grn.serializers import GRNMapSerializer,GRNDetailReadSerializer,GRNReadSerializer,GRNCreateBySerializer
from purchase_order.serializers import PurchaseMapSerializer
from company.serializers import CompanyListSerializer
from vendor.serializers import VendorAddressSerializer,VendorNameSerializer
from authentication.serializers import UserReadSerializer
from banks.serializers import BankSerializer




class PaymentMapSerializer(ModelSerializer):

    class Meta:
        model = PaymentMap
        fields = ['id','payment_no','is_deleted']



class PaymentSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    is_paid = serializers.BooleanField(default=False)
    special_note=serializers.CharField(required=False)




    class Meta:
        model = Payment
        fields = ['id','company','pur_inv','vendor','vendor_address','purchase_inv_no','purchase_inv_date','po_order','po_order_no','bank','payment_mode',
                  'payment_refrence','total_amount','special_note','is_approve','is_paid','status','created_at',
                  'created_by','is_deleted']



    def create(self, validated_data):



        payment = Payment.objects.create(**validated_data)

        payment_no = str(datetime.date.today()) + '/PAY-00' + str(payment.id)

        PaymentMap.objects.create(payment=payment,payment_no=payment_no)


        return payment

    def update(self, instance, validated_data):


            instance.company = validated_data.get('company', instance.company)
            instance.pur_inv = validated_data.get('pur_inv', instance.pur_inv)
            instance.vendor = validated_data.get('vendor', instance.vendor)
            instance.vendor_address = validated_data.get('vendor_address', instance.vendor_address)
            instance.purchase_inv_no = validated_data.get('purchase_inv_no', instance.purchase_inv_no)
            instance.purchase_inv_date = validated_data.get('purchase_inv_date', instance.purchase_inv_date)
            instance.po_order = validated_data.get('po_order', instance.po_order)
            instance.po_order_no = validated_data.get('po_order_no', instance.po_order_no)
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



    company = CompanyListSerializer()
    vendor = VendorNameSerializer(read_only=True)
    vendor_address = VendorAddressSerializer(read_only=True)
    created_by = UserReadSerializer()
    bank=BankSerializer()
    payment_map=PaymentMapSerializer(read_only=True,many=True)

    class Meta:
        model = Payment
        fields = ['id','company','pur_inv','vendor','vendor_address','purchase_inv_no','purchase_inv_date','po_order','po_order_no','bank','payment_mode',
                  'payment_refrence','total_amount','special_note','is_approve','is_paid','status','created_at',
                  'created_by','payment_map','is_deleted']



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
    payment_map = PaymentMapSerializer(read_only=True, many=True)

    class Meta:
        model = Payment
        fields = ['id','payment_map']