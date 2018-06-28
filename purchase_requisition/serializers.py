from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from purchase_requisition.models import RequisitionDetail,Requisition
from django.contrib.auth.models import User
import datetime
from company.serializers import CompanyListSerializer
from authentication.serializers import UserLoginSerializer,UserReadSerializer
from material_master.serializers import MaterialNameSerializer,MaterialReadSerializer,MaterialSerializer
from company_project.serializers import CompanyProjectSerializer,CompanyProjectDetailsSerializer
from uom.serializers import UOMSerializer
from rest_framework.relations import StringRelatedField,PrimaryKeyRelatedField
from company_project.serializers import CompanyProjectSerializer,CompanyProjectReadSerializer
from company_project.models import CompanyProjectDetail,CompanyProject
from appapprovepermission.models import AppApprove,EmpApprove,EmpApproveDetail
from django.db.models import Q
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import Context,Template
from mail.models import MailTemplate
from erp_tribeni.settings import SITE_URL
from rest_framework.authtoken.models import Token
import base64


class RequisitionMapSerializer(ModelSerializer):


    class Meta:
        model = Requisition
        fields = ['requisition_no']

class RequisitionDetailSerializer(ModelSerializer):

    #created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = RequisitionDetail
        fields = ['id','material_type','material','quantity','uom','status']



class RequisitionSerializer(ModelSerializer):
    requisition_detail=RequisitionDetailSerializer(many=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    # is_approve = serializers.BooleanField(default=False)
    # is_finalised = serializers.BooleanField(default=False)

    class Meta:
        model = Requisition
        fields = ['id','company','project','special_note','is_approve','is_finalised','status','created_at','created_by',
                  'requisition_detail']

    def create(self, validated_data):

            requisitions_data = validated_data.pop('requisition_detail')


            requisition = Requisition.objects.create(**validated_data)


            requisition_no=str(datetime.date.today())+'/I-00'+str(requisition.id)


            for requisition_data in requisitions_data:
                detail = RequisitionDetail.objects.create(requisition=requisition,**requisition_data)
                detail.avail_qty=detail.quantity
                detail.save()

                project = CompanyProjectDetail.objects.filter(project=detail.requisition.project,
                                                               material=detail.material)
                for i in project:
                    i.avail_qty = i.avail_qty - detail.quantity
                    i.save()


            requisition.requisition_no=requisition_no
            requisition.save()
            """***** Mail send *****"""



            #admin_user = User.objects.values_list('email', flat=True).filter(is_superuser=True)
            # for each_user in admin_user:
                # print(each_user)

            emp = EmpApproveDetail.objects.filter(emp_approve__content=29,emp_level=1)


            mail_list=list()

            for eachemp in emp:
                mail_list.append(eachemp.primary_emp.email)
                mail_list.append(eachemp.secondary_emp.email)

            mail_content=MailTemplate.objects.get(code='requisition_created')

            for each_mail in mail_list:
                username=User.objects.get(email=each_mail)
                token_data = Token.objects.filter(user=username)
                encode_token=''

                for i in token_data:
                    print(i.key)
                    encode_token = base64.b64encode(i.key.encode('utf-8')).decode()

                from_email='shyamdemo2018@gmail.com'
                text_link = SITE_URL + 'purchase-requisition/details/' + str(requisition.id)+ '/?token='+encode_token
                subject=mail_content.subject

                d = Context({'link': text_link,'name':username.first_name})
                text_content = Template(mail_content.text_content)
                html_content = Template(mail_content.html_content)

                text_content=text_content.render(d)
                html_content=html_content.render(d)


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

            return requisition

    def update(self, instance, validated_data):
            requisitions_data = validated_data.pop('requisition_detail')

            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)

            instance.save()

            return instance



class RequisitionDetailReadSerializer(ModelSerializer):

    #created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    material=MaterialNameSerializer(read_only=True)
    uom=UOMSerializer(read_only=True)


    class Meta:
        model = RequisitionDetail
        fields = ['id','material','quantity','avail_qty','uom','status','material_rate']


class RequisitionReadSerializer(ModelSerializer):

    requisition_detail=RequisitionDetailReadSerializer(many=True)
    company=CompanyListSerializer()
    created_by=UserReadSerializer()
    project=CompanyProjectReadSerializer()

    class Meta:
        model = Requisition
        fields = ['id','company','special_note','is_approve','is_finalised','status','created_at','created_by',
                  'requisition_detail','requisition_no','project','approval_level']


class RequisitionUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = Requisition
        fields = ['id','status','is_approve','is_finalised','approval_level']

    def update(self, instance, validated_data):

        if validated_data.get('is_finalised') == '1':
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.save()


        else:

            user = self.context['request'].user
            print(validated_data.get('approval_level'))
            emp=EmpApprove.objects.filter(Q(content=29),
                                          Q(emp_approve_details__emp_level=validated_data.get('approval_level')),
                                          (Q(emp_approve_details__primary_emp=user)|Q(emp_approve_details__secondary_emp=user)))

            if validated_data.get('is_approve') == '2':
                emp = EmpApprove.objects.filter(Q(content=29),
                                                (Q(emp_approve_details__primary_emp=user) | Q(
                                                    emp_approve_details__secondary_emp=user)))

                requisition_detail=RequisitionDetail.objects.filter(requisition=instance)

                for i in requisition_detail:
                    project = CompanyProjectDetail.objects.filter(project=instance.project,
                                                                  material=i.material)
                    for project_data in project:
                        project_data.avail_qty += i.quantity
                        project_data.save()
                        if project_data.project.is_finalised == '1' :

                            main_project=CompanyProject.objects.get(id=project_data.project.id)
                            main_project.is_finalised='0'
                            main_project.save()

            if emp:

                app_level=AppApprove.objects.filter(content__model='requisition')

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

                emp = EmpApproveDetail.objects.filter(emp_approve__content=29, emp_level=validated_data.get('approval_level')+1)
                print(emp.query)

                mail_list = list()
                for eachemp in emp:
                    mail_list.append(eachemp.primary_emp.email)
                    mail_list.append(eachemp.secondary_emp.email)

                mail_content = MailTemplate.objects.get(code='requisition_updated')

                for each_mail in mail_list:
                    username = User.objects.get(email=each_mail)
                    token_data = Token.objects.filter(user=username)
                    encode_token = ''

                    for i in token_data:
                        print(i.key)
                        encode_token = base64.b64encode(i.key.encode('utf-8')).decode()

                    from_email = 'shyamdemo2018@gmail.com'
                    text_link = SITE_URL + 'purchase-requisition/details/' + str(instance.id) + '/?token=' + encode_token
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




class RequisitionDetailReadForPreviuosPurchaseSerializer(ModelSerializer):

    #created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    material=MaterialNameSerializer(read_only=True)
    uom=UOMSerializer(read_only=True)


    class Meta:
        model = RequisitionDetail
        fields = ['id','material','quantity','uom','status','material_rate','project_material_quantity']


class RequisitionReadSerializerForPreviuosPurchase(ModelSerializer):

    requisition_detail=RequisitionDetailReadForPreviuosPurchaseSerializer(many=True)
    company=CompanyListSerializer()
    created_by=UserReadSerializer()
    project=CompanyProjectReadSerializer()

    class Meta:
        model = Requisition
        fields = ['id','company','special_note','is_approve','is_finalised','status','created_at','created_by',
                  'requisition_detail','requisition_no','project']


class RequisitionProjectNameSerializer(ModelSerializer):

    class Meta:
        model = Requisition
        fields = ['id','requisition_number','project_id','project_name']
