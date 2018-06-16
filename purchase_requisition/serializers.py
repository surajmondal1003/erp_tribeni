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
from company_project.models import CompanyProjectDetail
from appapprovepermission.models import AppApprove,EmpApprove
from django.db.models import Q


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
                #req_qty=detail.quantity
                #material=CompanyProjectDetail.objects.values_list('id','material','avail_qty').filter(material=detail.material,compan)
                #print(material.query)
                # project_qty=0
                # for i in material.values_list('avail_qty'):
                #     project_qty=i
                #
                # avail_qty=project_qty[0]-req_qty
                # #print(project_qty[0])
                # print(avail_qty)

                # for obj in material:
                #     obj.avail_qty = avail_qty
                #     obj.save()

            requisition.requisition_no=requisition_no
            requisition.save()




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
                  'requisition_detail','requisition_no','project']


class RequisitionUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = Requisition
        fields = ['id','status','is_approve','is_finalised','approval_level']

    def update(self, instance, validated_data):

            user = self.context['request'].user
            emp=EmpApprove.objects.filter(Q(content__model='requisition'),Q(emp_level=validated_data.get('approval_level')),(Q(primary_emp=user)|Q(secondary_emp=user)))
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
