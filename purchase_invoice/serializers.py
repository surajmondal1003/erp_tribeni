from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from company_branch.serializers import UOMSerializer
import datetime

from purchase_invoice.models import PurchaseInvoice,PurchaseInvoiceDetail,PurchaseInvoiceMap
from django.contrib.auth.models import User
from grn.serializers import GRNMapSerializer,GRNDetailReadSerializer,GRNReadSerializer,GRNCreateBySerializer
from purchase_order.serializers import PurchaseMapSerializer,PurchaseDetailSerializer
from company.serializers import CompanyListSerializer
from material_master.serializers import MaterialNameSerializer
from vendor.serializers import VendorNameSerializer,VendorAddressSerializer
from purchaseorggroup.serializers import PurchaseOrgSerializer,PurchaseGroupSerializer
from django.core.mail import send_mail


class PurchaseInvoiceMapSerializer(ModelSerializer):

    class Meta:
        model = PurchaseInvoiceMap
        fields = ['id','purchase_inv_no']




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
        fields = ['id','grn','po_order','pur_org','pur_grp','total_gst','total_amount','vendor','vendor_address',
                  'company','is_approve','is_finalised','status','created_at','created_by',
                  'pur_invoice_detail']


    def create(self, validated_data):

        purchase_invoice_detail_data = validated_data.pop('pur_invoice_detail')

        po_invoice = PurchaseInvoice.objects.create(**validated_data)

        purchase_invoice_no = str(datetime.date.today()) + '/INV-00' + str(po_invoice.id)

        for purchase_invoice_detail in purchase_invoice_detail_data:
            PurchaseInvoiceDetail.objects.create(pur_invoice=po_invoice, **purchase_invoice_detail)


        PurchaseInvoiceMap.objects.create(pur_invoice=po_invoice, purchase_inv_no=purchase_invoice_no)



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
    grn_number = GRNMapSerializer(read_only=True,many=True)
    pur_invoice_detail=PurchaseInvoiceReadDetailSerializer(many=True)
    pur_invoice_map=PurchaseInvoiceMapSerializer(many=True)
    po_order_no = PurchaseMapSerializer(many=True,read_only=True)
    pur_org = PurchaseOrgSerializer()
    pur_grp = PurchaseGroupSerializer()
    company = CompanyListSerializer()
    vendor = VendorNameSerializer(read_only=True)
    vendor_address = VendorAddressSerializer()

    class Meta:
        model = PurchaseInvoice
        fields = ['id','grn','grn_number',  'po_order','po_order_no','pur_org','pur_grp','total_gst','total_amount','vendor','vendor_address',
                  'company','is_approve','is_finalised','status','created_at','created_by',
                  'pur_invoice_detail','pur_invoice_map']



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
