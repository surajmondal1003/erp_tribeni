from company_project.models import CompanyProject, CompanyProjectDetail
from states.models import State
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

class CompanyProjectSerializer(ModelSerializer):
    project_name = serializers.CharField(
        validators=[UniqueValidator(queryset=CompanyProject.objects.all())]
    )

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.BooleanField(default=True)

    class Meta:
        model = CompanyProject
        fields = ['id','company','project_name','description','project_address','project_state','project_city','project_pincode',
                  'project_contact_no','contact_person','project_gstin','engineer_name','engineer_contact_no','status','created_at','created_by','is_deleted']

class CompanyProjectDetailsSerializer(ModelSerializer):
    class Meta:
        model = CompanyProjectDetail
        fields = ['id','project','materialtype','material','quantity','boq_ref']






