from company.models import Company,TermsandConditon
from states.models import State
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator



class ChildrenSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data



class CompanySerializer(ModelSerializer):
    company_name = serializers.CharField(
        validators=[UniqueValidator(queryset=Company.objects.all())]
    )

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status=serializers.BooleanField(default=True)
    children=ChildrenSerializer(many=True, read_only=True)
    company_url = serializers.CharField(required=False, allow_blank=True)  # Not mandatory field
    company_gst = serializers.CharField(required=False, allow_blank=True)  # Not mandatory field
    company_pan = serializers.CharField(required=False, allow_blank=True)  # Not mandatory field
    company_cin = serializers.CharField(required=False, allow_blank=True)  # Not mandatory field
    company_email = serializers.EmailField(required=False, allow_blank=True)  # Not mandatory field

    class Meta:
        model = Company
        fields = ['id','parent','company_name','company_url','company_gst','company_pan','company_cin','company_email',
                  'company_address','company_contact','company_state','company_city','company_pin','status','created_at',
                  'created_by','is_deleted','children']

class CompanyListSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','company_name']




class TermsAndConditionSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    class Meta:
        model = TermsandConditon
        fields = ['id','company','term_type','term_text','status','created_at','created_by','is_deleted']


class TermsAndConditionReadSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    company=CompanyListSerializer()
    class Meta:
        model = TermsandConditon
        fields = ['id','company','term_type','term_text','status','created_at','created_by','is_deleted']