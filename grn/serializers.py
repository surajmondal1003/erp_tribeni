from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
import datetime

from grn.models import GRN,GRNDetail,ReversGRN,ReverseGRNDetail
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
from purchase_order.models import PurchaseOrderDetail
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
            detail=GRNDetail.objects.create(grn=grn, **grn_detail)
            order = PurchaseOrderDetail.objects.filter(po_order=detail.grn.po_order,
                                                           material=detail.material)
            for i in order:
                i.avail_qty = i.avail_qty - detail.receive_quantity
                i.save()

        grn.grn_no = grn_no
        grn.save()

        """***** Mail send *****"""

        # admin_user = User.objects.values_list('email', flat=True).filter(is_superuser=True)
        # for each_user in admin_user:
        # print(each_user)

        emp = EmpApproveDetail.objects.filter(emp_approve__content=35, emp_level=1)
        print(emp.query)

        mail_list = list()
        for eachemp in emp:
            mail_list.append(eachemp.primary_emp.email)
            mail_list.append(eachemp.secondary_emp.email)

        mail_content = MailTemplate.objects.get(code='grn_created')

        for each_mail in mail_list:
            username = User.objects.get(email=each_mail)
            token_data = Token.objects.filter(user=username)
            encode_token = ''

            for i in token_data:
                print(i.key)
                encode_token = base64.b64encode(i.key.encode('utf-8')).decode()

            from_email = 'shyamdemo2018@gmail.com'
            text_link = SITE_URL + 'grn/details/' + str(grn.id) + '/?token=' + encode_token
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
                  'created_by','grn_detail','is_deleted','purchase_order_no','project']


class GRNCreateBySerializer(ModelSerializer):
    created_by = UserReadSerializer()

    class Meta:
        model = GRN
        fields = ['id','created_at','created_by']




class GRNUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = GRN
        fields = ['id','status','is_approve','is_finalised','is_deleted','approval_level']


    def update(self, instance, validated_data):

            user = self.context['request'].user
            emp=EmpApprove.objects.filter(Q(content=35),
                                          Q(emp_approve_details__emp_level=validated_data.get('approval_level')),
                                          (Q(emp_approve_details__primary_emp=user)|Q(emp_approve_details__secondary_emp=user)))

            if validated_data.get('is_approve') == '2':
                emp = EmpApprove.objects.filter(Q(content=35),
                                                (Q(emp_approve_details__primary_emp=user) | Q(
                                                    emp_approve_details__secondary_emp=user)))

                grn_detail = GRNDetail.objects.filter(grn=instance)

                for i in grn_detail:
                    po_detail = PurchaseOrderDetail.objects.filter(po_order=instance.po_order,
                                                                  material=i.material)
                    for po_data in po_detail:
                        po_data.avail_qty += i.receive_quantity
                        po_data.save()
                        if po_data.po_order.is_finalised == '1':
                            po_data.po_order.is_finalised = '0'
                            po_data.save()

            if emp:

                app_level=AppApprove.objects.filter(content=35)

                instance.is_approve = validated_data.get('is_approve', instance.is_approve)
                instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
                instance.status = validated_data.get('status', instance.status)
                instance.approval_level=validated_data.get('approval_level',instance.approval_level)

                approval_level=0
                for i in app_level:
                    approval_level=i.approval_level

                if instance.approval_level == approval_level:
                    instance.is_approve='1'
                instance.save()

                text_message = 'http://132.148.130.125:8000/grn_status/' + str(instance.id) + '/'

                emp = EmpApproveDetail.objects.filter(emp_approve__content=35, emp_level=validated_data.get('approval_level')+1)


                mail_list = list()
                for eachemp in emp:
                    mail_list.append(eachemp.primary_emp.email)
                    mail_list.append(eachemp.secondary_emp.email)

                mail_content = MailTemplate.objects.get(code='grn_updated')

                for each_mail in mail_list:
                    username = User.objects.get(email=each_mail)
                    token_data = Token.objects.filter(user=username)
                    encode_token = ''

                    for i in token_data:
                        print(i.key)
                        encode_token = base64.b64encode(i.key.encode('utf-8')).decode()

                    from_email = 'shyamdemo2018@gmail.com'
                    text_link = SITE_URL + 'grn/details/' + str(instance.id) + '/?token=' + encode_token
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
                raise serializers.ValidationError({'message':'You dont have authority to Approve'})

            return instance




class ReverseGRNDetailSerializer(ModelSerializer):

    class Meta:
        model = ReverseGRNDetail
        fields = ['id','material','reverse_grn_quantity','reverse_reason']




class ReversGRNSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    reverse_grn_detail=ReverseGRNDetailSerializer(many=True)


    class Meta:
        model = ReversGRN
        fields = ['id','grn','created_at','created_by','status','is_approve','is_finalised','reverse_grn_detail']


    def create(self, validated_data):

        reverse_grn_detail = validated_data.pop('reverse_grn_detail')

        revers_grn = ReversGRN.objects.create(**validated_data)

        revers_gen_no = str(datetime.date.today()) + '/REGRN-00' + str(revers_grn.id)

        revers_grn.revers_gen_no = revers_gen_no
        revers_grn.save()

        for reverse_grn_data in reverse_grn_detail:
            reverse_detail=ReverseGRNDetail.objects.create(reverse_grn=revers_grn, **reverse_grn_data)

            grn_detail = GRNDetail.objects.filter(grn=revers_grn.grn,material=reverse_detail.material)
            for i in grn_detail:
                i.receive_quantity = i.receive_quantity - reverse_detail.reverse_grn_quantity
                i.save()

        """***** Mail send *****"""
        text_message = 'http://132.148.130.125:8000/reversegrn_status/' + str(revers_grn.id) + '/'

        # admin_user = User.objects.values_list('email', flat=True).filter(is_superuser=True)
        # for each_user in admin_user:
        # print(each_user)

        emp = EmpApproveDetail.objects.filter(emp_approve__content=37, emp_level=1)
        print(emp.query)

        mail_list = list()
        for eachemp in emp:
            mail_list.append(eachemp.primary_emp.email)
            mail_list.append(eachemp.secondary_emp.email)

        mail_content = MailTemplate.objects.get(code='reverse_grn_created')

        for each_mail in mail_list:
            username = User.objects.get(email=each_mail)
            token_data = Token.objects.filter(user=username)
            encode_token = ''

            for i in token_data:
                print(i.key)
                encode_token = base64.b64encode(i.key.encode('utf-8')).decode()

            from_email = 'shyamdemo2018@gmail.com'
            text_link = SITE_URL + 'grn/details/' + str(revers_grn.id) + '/?token=' + encode_token
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

        return revers_grn

    def update(self, instance, validated_data):

            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)

            instance.save()

            return instance



class ReverseGRNDetailReadSerializer(ModelSerializer):

    class Meta:
        model = ReverseGRNDetail
        fields = ['id','material_details','material_uom','reverse_grn_quantity','reverse_reason']


class ReversGRNReadSerializer(ModelSerializer):
    reverse_grn_detail = ReverseGRNDetailReadSerializer(many=True)
    created_by = UserReadSerializer()
    class Meta:
        model = ReversGRN
        fields = ['id', 'grn','revers_gen_no','created_at','created_by','status','is_approve',
                  'is_finalised','reverse_grn_detail','grn_no','company','vendor_name','vendor_address','project',
                  'purchase_order_no','approval_level']





class ReverseGRNUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = ReversGRN
        fields = ['id','status','is_approve','is_finalised','approval_level']


    def update(self, instance, validated_data):

            user = self.context['request'].user
            emp=EmpApprove.objects.filter(Q(content=37),
                                          Q(emp_approve_details__emp_level=validated_data.get('approval_level')),
                                          (Q(emp_approve_details__primary_emp=user)|Q(emp_approve_details__secondary_emp=user)))

            if validated_data.get('is_approve') == '2':
                emp = EmpApprove.objects.filter(Q(content=37),
                                                (Q(emp_approve_details__primary_emp=user) | Q(
                                                    emp_approve_details__secondary_emp=user)))

                reverse_grn_detail = ReverseGRNDetail.objects.filter(reverse_grn=instance)

                for reverse_detail in reverse_grn_detail:
                    grn_detail = GRNDetail.objects.filter(grn=instance.grn, material=reverse_detail.material)
                    for i in grn_detail:
                        i.receive_quantity = i.receive_quantity + reverse_detail.reverse_grn_quantity
                        i.save()

            if emp:

                app_level=AppApprove.objects.filter(content=37)

                instance.is_approve = validated_data.get('is_approve', instance.is_approve)
                instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
                instance.status = validated_data.get('status', instance.status)
                instance.approval_level=validated_data.get('approval_level',instance.approval_level)

                approval_level=0
                for i in app_level:
                    approval_level=i.approval_level

                if instance.approval_level == approval_level:
                    instance.is_approve='1'
                instance.save()

                #text_message = 'http://132.148.130.125:8000/reversegrn_status/' + str(instance.id) + '/'

                emp = EmpApproveDetail.objects.filter(emp_approve__content=37, emp_level=validated_data.get('approval_level')+1)
                print(emp.query)

                mail_list = list()
                for eachemp in emp:
                    mail_list.append(eachemp.primary_emp.email)
                    mail_list.append(eachemp.secondary_emp.email)

                mail_content = MailTemplate.objects.get(code='reverse_grn_updated')

                for each_mail in mail_list:
                    username = User.objects.get(email=each_mail)
                    token_data = Token.objects.filter(user=username)
                    encode_token = ''

                    for i in token_data:
                        print(i.key)
                        encode_token = base64.b64encode(i.key.encode('utf-8')).decode()

                    from_email = 'shyamdemo2018@gmail.com'
                    text_link = SITE_URL + 'grn/details/' + str(instance.id) + '/?token=' + encode_token
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
                raise serializers.ValidationError({'message':'You dont have authority to Approve'})

            return instance