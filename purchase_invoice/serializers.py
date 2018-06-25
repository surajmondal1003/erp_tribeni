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
from appapprovepermission.models import AppApprove,EmpApprove,EmpApproveDetail
from django.db.models import Q




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
        fields = ['id','grn','total_gst','total_amount','vendor','vendor_address',
                  'company','is_approve','is_finalised','status','created_at','created_by',
                  'pur_invoice_detail','purchase_inv_no']

    def create(self, validated_data):

        purchase_invoice_detail_data = validated_data.pop('pur_invoice_detail')

        po_invoice = PurchaseInvoice.objects.create(**validated_data)


        for purchase_invoice_detail in purchase_invoice_detail_data:
            PurchaseInvoiceDetail.objects.create(pur_invoice=po_invoice, **purchase_invoice_detail)

        """***** Mail send *****"""
        text_message = 'http://132.148.130.125:8000/purchase_invoice_status/' + str(po_invoice.id) + '/'

        emp = EmpApproveDetail.objects.filter(emp_approve__content=38, emp_level=1)
        print(emp.query)

        mail_list = list()
        for eachemp in emp:
            mail_list.append(eachemp.primary_emp.email)
            mail_list.append(eachemp.secondary_emp.email)
        print(mail_list)

        send_mail(
            'Test Subject',
            text_message,
            'shyamdemo2018@gmail.com',
            mail_list,
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
        fields = ['id','grn','total_gst','total_amount','vendor','vendor_address',
                  'company','is_approve','is_finalised','status','created_at','created_by',
                  'pur_invoice_detail','purchase_inv_no','grn_number','po_order_no','project_name','approval_level']



class InvoiceUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = PurchaseInvoice
        fields = ['id','status','is_approve','is_finalised','approval_level']


    def update(self, instance, validated_data):
        user = self.context['request'].user
        emp = EmpApprove.objects.filter(Q(content=34),
                                        Q(emp_approve_details__emp_level=validated_data.get('approval_level')),
                                        (Q(emp_approve_details__primary_emp=user) | Q(
                                            emp_approve_details__secondary_emp=user)))

        if validated_data.get('is_approve') == '2':
            emp = EmpApprove.objects.filter(Q(content=34),
                                            (Q(emp_approve_details__primary_emp=user) | Q(
                                                emp_approve_details__secondary_emp=user)))

            # inv_detail = PurchaseInvoiceDetail.objects.filter(pur_invoice=instance)
            #
            # for i in inv_detail:
            #     po_detail = PurchaseOrderDetail.objects.filter(po_order=instance.po_order,
            #
            #                       material=i.material)
            #     for po_data in po_detail:
            #         po_data.avail_qty += i.receive_quantity
            #         po_data.save()
            #         if po_data.po_order.is_finalised == '1':
            #             po_data.po_order.is_finalised = '0'
            #             po_data.save()

        if emp:

            app_level = AppApprove.objects.filter(content=34)

            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)
            instance.approval_level = validated_data.get('approval_level', instance.approval_level)

            approval_level = 0
            for i in app_level:
                approval_level = i.approval_level

            if instance.approval_level == approval_level:
                instance.is_approve = '1'
            instance.save()

            text_message = 'http://132.148.130.125:8000/purchase_invoice_status/' + str(instance.id) + '/'

            emp = EmpApproveDetail.objects.filter(emp_approve__content=34,
                                                  emp_level=validated_data.get('approval_level') + 1)
            print(emp.query)

            mail_list = list()
            for eachemp in emp:
                mail_list.append(eachemp.primary_emp.email)
                mail_list.append(eachemp.secondary_emp.email)
            print(mail_list)

            send_mail(
                'Test Subject',
                text_message,
                'shyamdemo2018@gmail.com',
                mail_list,
                fail_silently=False,
            )


        else:
            raise serializers.ValidationError({'message': 'You dont have authority to Approve'})

        return instance
