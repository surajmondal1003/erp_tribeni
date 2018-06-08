from company_project.models import CompanyProject, CompanyProjectDetail
from states.models import State
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from material_master.serializers import MaterialNameSerializer,MaterialTypeSerializer
from states.serializers import StateNameSerializer



class CompanyProjectDetailsSerializer(ModelSerializer):
    material = MaterialNameSerializer(read_only=True)
    materialtype = MaterialTypeSerializer(read_only=True)
    class Meta:
        model = CompanyProjectDetail
        fields = ['id','materialtype','material','quantity','boq_ref','rate']







class CompanyProjectSerializer(ModelSerializer):
    project_name = serializers.CharField()
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.BooleanField(default=True)
    project_details=CompanyProjectDetailsSerializer(many=True)
    #project_contact_no=serializers.IntegerField(required=False,allow_null=True,allow_bla)

    class Meta:
        model = CompanyProject
        fields = ['id','company','project_name','description','project_address','project_state','project_city','project_pincode',
                  'project_contact_no','contact_person','project_gstin','engineer_name','engineer_contact_no','status','created_at',
                  'created_by','is_deleted','is_approve','is_finalised','project_details']


    def create(self, validated_data):

            project_details_data = validated_data.pop('project_details')
            project = CompanyProject.objects.create(**validated_data)

            for details_data in project_details_data:
                detail=CompanyProjectDetail.objects.create(project=project,**details_data)
                detail.avail_qty=detail.quantity
                detail.save()

            return project


class CompanyProjectUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = CompanyProject
        fields = ['id','status','is_deleted','is_approve','is_finalised']


    def update(self, instance, validated_data):
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.status = validated_data.get('status', instance.status)
            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.save()

            return instance



class CompanyProjectDetailsReadSerializer(ModelSerializer):

    class Meta:
        model = CompanyProjectDetail
        fields = ['id','project','materialtype','material','quantity','boq_ref','rate']


class CompanyProjectReadSerializer(ModelSerializer):
    project_name = serializers.CharField()
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.BooleanField(default=True)
    project_details=CompanyProjectDetailsReadSerializer(many=True)
    #project_contact_no=serializers.IntegerField(required=False,allow_null=True,allow_bla)
    project_state=StateNameSerializer(read_only=True,many=True)
    class Meta:
        model = CompanyProject
        fields = ['id','company','project_name','description','project_address','project_state','project_city','project_pincode',
                  'project_contact_no','contact_person','project_gstin','engineer_name','engineer_contact_no','status','created_at',
                  'created_by','is_deleted','is_approve','is_finalised','project_details']
