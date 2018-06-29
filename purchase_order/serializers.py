from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from uom.serializers import UOMSerializer
import datetime
from purchase_order.models import PurchaseOrderTerms,PurchaseOrderFreight,PurchaseOrderDetail,PurchaseOrder
from material_master.serializers import MaterialNameSerializer
from company.serializers import CompanyListSerializer,TermsAndConditionSerializer
from authentication.serializers import UserReadSerializer
from company_project.serializers import CompanyProjectSerializer,CompanyProjectDetailsSerializer
from rest_framework.relations import StringRelatedField
from vendor.serializers import VendorAddressSerializer,VendorNameSerializer
from purchase_requisition.models import Requisition,RequisitionDetail
from purchase_requisition.serializers import RequisitionProjectNameSerializer
from appapprovepermission.models import AppApprove,EmpApprove,EmpApproveDetail
from django.db.models import Q
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context,Template
from mail.models import MailTemplate
from erp_tribeni.settings import SITE_URL
from rest_framework.authtoken.models import Token
import base64
from django.contrib.auth.models import User



class PurchaseTermsSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrderTerms
        fields = ['id','po_terms']


class PurchaseFreightSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrderFreight
        fields = ['id','freight_option','vendor','freight_rate','freight_amount','freight_gst_rate','freight_total']



class PurchaseDetailSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrderDetail
        fields = ['id','material','uom','requisition_quantity',
                  'order_quantity', 'rate', 'material_value', 'discount_percent', 'discount_value', 'igst',
                  'cgst','sgst', 'gst_amount', 'sub_total', 'delivery_date']




class PurchaseOrderSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    purchase_order_detail = PurchaseDetailSerializer(many=True)
    purchase_order_freight = PurchaseFreightSerializer(many=True)
    purchase_order_terms = PurchaseTermsSerializer(many=True)


    class Meta:
        model = PurchaseOrder
        fields = ['id','requisition','quotation_no','quotation_date','company','vendor','vendor_address',
                  'grand_total','grand_total_words','is_approve','is_finalised','status','created_at','created_by',
                  'purchase_order_detail','purchase_order_freight','purchase_order_terms']



    def create(self, validated_data):

        purchase_order_detail_data = validated_data.pop('purchase_order_detail')
        purchase_order_freight_data = validated_data.pop('purchase_order_freight')
        purchase_order_terms_data = validated_data.pop('purchase_order_terms')


        po_order = PurchaseOrder.objects.create(**validated_data)

        purchase_order_no = str(datetime.date.today()) + '/O-00' + str(po_order.id)

        for purchase_order_detail in purchase_order_detail_data:
            detail=PurchaseOrderDetail.objects.create(po_order=po_order, **purchase_order_detail)
            detail.avail_qty=detail.order_quantity
            detail.save()

            requisition=RequisitionDetail.objects.filter(requisition=detail.po_order.requisition,material=detail.material)
            for i in requisition:
                avail_qty=i.avail_qty - detail.order_quantity
                if avail_qty < 0:
                    i.avail_qty=0
                else:
                    i.avail_qty=avail_qty
                i.save()

        for purchase_order_freight in purchase_order_freight_data:
            PurchaseOrderFreight.objects.create(po_order=po_order, **purchase_order_freight)
        for purchase_order_terms in purchase_order_terms_data:
            PurchaseOrderTerms.objects.create(po_order=po_order, **purchase_order_terms)

        po_order.purchase_order_no = purchase_order_no
        po_order.save()

        """***** Mail send *****"""


        emp = EmpApproveDetail.objects.filter(emp_approve__content=35, emp_level=1)
        print(emp.query)

        mail_list = list()
        for eachemp in emp:
            mail_list.append(eachemp.primary_emp.email)
            mail_list.append(eachemp.secondary_emp.email)

        mail_content = MailTemplate.objects.get(code='order_created')

        for each_mail in mail_list:
            username = User.objects.get(email=each_mail)
            token_data = Token.objects.filter(user=username)
            encode_token = ''

            for i in token_data:
                print(i.key)
                encode_token = base64.b64encode(i.key.encode('utf-8')).decode()

            from_email = 'shyamdemo2018@gmail.com'
            text_link = SITE_URL + 'purchase-orders/details/' + str(po_order.id) + '/?token=' + encode_token
            subject = mail_content.subject

            d = Context({'link': text_link, 'name': username.first_name})
            text_content = Template(mail_content.text_content)
            html_content = Template(mail_content.html_content)

            text_content = text_content.render(d)
            html_content = html_content.render(d)

            msg = EmailMultiAlternatives(subject, text_content, from_email, [each_mail])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # send_mail(
            #     'Test Subject',
            #     text_message,
            #     'shyamdemo2018@gmail.com',
            #     mail_list,
            #     fail_silently=False,
            # )


        return po_order


    def update(self, instance, validated_data):
            purchase_order_detail_data = validated_data.pop('purchase_order_detail')
            purchase_order_freight_data = validated_data.pop('purchase_order_freight')
            purchase_order_terms_data = validated_data.pop('purchase_order_terms')

            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)

            instance.save()

            return instance




class PurchaseDetailReadSerializer(ModelSerializer):

    material=MaterialNameSerializer(read_only=True)
    uom=UOMSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderDetail
        fields = ['id','material','uom','requisition_quantity',
                  'order_quantity', 'rate', 'material_value', 'discount_percent', 'discount_value', 'igst',
                  'cgst','sgst', 'gst_amount', 'sub_total', 'delivery_date','avail_qty']



class PurchseTermsReadSerializer(ModelSerializer):
    po_terms=TermsAndConditionSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderTerms
        fields = ['id','po_terms']


class PurchaseOrderReadSerializer(ModelSerializer):
    company=CompanyListSerializer()
    created_by=UserReadSerializer()
    purchase_order_detail = PurchaseDetailReadSerializer(many=True)
    purchase_order_freight = PurchaseFreightSerializer(many=True)
    purchase_order_terms = PurchseTermsReadSerializer(many=True)
    vendor=VendorNameSerializer(read_only=True)
    vendor_address=VendorAddressSerializer(read_only=True)
    requisition=RequisitionProjectNameSerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id','quotation_no','quotation_date','company','vendor','vendor_address',
                  'grand_total','grand_total_words','is_approve','is_finalised','status','created_at','created_by',
                  'purchase_order_detail','purchase_order_freight','purchase_order_terms','purchase_order_no',
                  'requisition','approval_level','project']


class PurchaseDetailReadForGRNSerializer(ModelSerializer):
    material=MaterialNameSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderDetail
        fields = ['id','material','uom','requisition_quantity',
                  'order_quantity', 'rate', 'material_value', 'discount_percent', 'discount_value', 'igst',
                  'cgst','sgst', 'gst_amount', 'sub_total', 'delivery_date','avail_qty']



class PurchaseOrderReadForGRNSerializer(ModelSerializer):

    purchase_order_detail = PurchaseDetailReadSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id','purchase_order_detail']

class PurchaseOrderUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['id','status','is_approve','is_finalised','approval_level']


    def update(self, instance, validated_data):

        if validated_data.get('is_finalised') == '1':
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.save()


        else:

            user = self.context['request'].user

            emp = EmpApprove.objects.filter(Q(content=34),
                                            Q(emp_approve_details__emp_level=validated_data.get('approval_level')),
                                            (Q(emp_approve_details__primary_emp=user) | Q(
                                                emp_approve_details__secondary_emp=user)))

            if validated_data.get('is_approve') == '2':
                emp = EmpApprove.objects.filter(Q(content=34),
                                                (Q(emp_approve_details__primary_emp=user) | Q(
                                                    emp_approve_details__secondary_emp=user)))

                order_detail = PurchaseOrderDetail.objects.filter(po_order=instance)

                for i in order_detail:


                    requisition = RequisitionDetail.objects.filter(requisition=instance.requisition,
                                                                  material=i.material)
                    for requisition_data in requisition:
                        requisition_data.avail_qty += i.order_quantity
                        requisition_data.save()
                        if requisition_data.requisition.is_finalised == '1':
                            main_requisition=Requisition.objects.get(id=requisition_data.requisition.id)
                            main_requisition.is_finalised = '0'
                            main_requisition.save()

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


                emp = EmpApproveDetail.objects.filter(emp_approve__content=34,
                                                      emp_level=validated_data.get('approval_level') + 1)


                mail_list = list()
                for eachemp in emp:
                    mail_list.append(eachemp.primary_emp.email)
                    mail_list.append(eachemp.secondary_emp.email)

                mail_content = MailTemplate.objects.get(code='order_updated')

                for each_mail in mail_list:
                    username = User.objects.get(email=each_mail)
                    token_data = Token.objects.filter(user=username)
                    encode_token = ''

                    for i in token_data:
                        print(i.key)
                        encode_token = base64.b64encode(i.key.encode('utf-8')).decode()

                    from_email = 'shyamdemo2018@gmail.com'
                    text_link = SITE_URL + 'purchase-orders/details/' + str(instance.id) + '/?token=' + encode_token
                    subject = mail_content.subject

                    d = Context({'link': text_link, 'name': username.first_name})
                    text_content = Template(mail_content.text_content)
                    html_content = Template(mail_content.html_content)

                    text_content = text_content.render(d)
                    html_content = html_content.render(d)

                    msg = EmailMultiAlternatives(subject, text_content, from_email, [each_mail])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    # send_mail(
                    #     'Test Subject',
                    #     text_message,
                    #     'shyamdemo2018@gmail.com',
                    #     mail_list,
                    #     fail_silently=False,
                    # )


            else:
                raise serializers.ValidationError({'message': 'You dont have authority to Approve'})

        return instance
