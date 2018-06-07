from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from uom.serializers import UOMSerializer
import datetime
from purchase_invoice.models import PurchaseInvoice,PurchaseInvoiceDetail
from django.contrib.auth.models import User
from grn.serializers import GRNDetailReadSerializer,GRNReadSerializer,GRNCreateBySerializer
from purchase_order.serializers import PurchaseDetailSerializer,PurchaseOrderSerializer
from company.serializers import CompanyListSerializer
from material_master.serializers import MaterialNameSerializer
from vendor.serializers import VendorNameSerializer,VendorAddressSerializer
from django.core.mail import send_mail



class PurchaseInvoiceDetailSerializer(ModelSerializer):

    class Meta:
        model = PurchaseInvoiceDetail
        fields = ['id','material','rate','quantity','discount_per','discount_amount','igst',
                  'cgst', 'sgst', 'total_gst', 'material_value', 'material_amount_pay']



class PurchaseInvoiceSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    pur_invoice_detail = PurchaseInvoiceDetailSerializer(many=True)


    class Meta:
        model = PurchaseInvoice
        fields = ['id','grn','po_order','total_gst','total_amount','vendor','vendor_address',
                  'company','is_approve','is_finalised','status','created_at','created_by',
                  'pur_invoice_detail','purchase_inv_no']

    def create(self, validated_data):

        purchase_invoice_detail_data = validated_data.pop('pur_invoice_detail')

        po_invoice = PurchaseInvoice.objects.create(**validated_data)


        for purchase_invoice_detail in purchase_invoice_detail_data:
            PurchaseInvoiceDetail.objects.create(pur_invoice=po_invoice, **purchase_invoice_detail)



        text_message='http://192.168.24.208:8000/purchase_invoice_status/'+str(po_invoice.id)+'/'

        admin_user=User.objects.values_list('email',flat=True).filter(is_superuser=True)
        for each_user in admin_user:
            #print(each_user)
            send_mail(
                'Test Subject',
                text_message,
                'surajmondal1003@gmail.com',
                [ each_user ],
                fail_silently=False,
            )

        return po_invoice

    def update(self, instance, validated_data):

        instance.is_approve = validated_data.get('is_approve', instance.is_approve)
        instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
        instance.status = validated_data.get('status', instance.status)

        instance.save()

        return instance




class PurchaseInvoiceReadDetailSerializer(ModelSerializer):
    material = MaterialNameSerializer(read_only=True)

    class Meta:
        model = PurchaseInvoiceDetail
        fields = ['id','material','rate','quantity','discount_per','discount_amount','igst',
                  'cgst', 'sgst', 'total_gst', 'material_value', 'material_amount_pay']


class PurchaseInvoiceReadSerializer(ModelSerializer):


    grn= GRNCreateBySerializer(read_only=True)
    pur_invoice_detail=PurchaseInvoiceReadDetailSerializer(many=True)
    company = CompanyListSerializer()
    vendor = VendorNameSerializer(read_only=True)
    vendor_address = VendorAddressSerializer()

    class Meta:
        model = PurchaseInvoice
        fields = ['id','grn','po_order','total_gst','total_amount','vendor','vendor_address',
                  'company','is_approve','is_finalised','status','created_at','created_by',
                  'pur_invoice_detail','purchase_inv_no','po_order_no','grn_number']



class InvoiceUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = PurchaseInvoice
        fields = ['id','status','is_approve','is_finalised']


    def update(self, instance, validated_data):
            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)
            instance.save()

            return instance
