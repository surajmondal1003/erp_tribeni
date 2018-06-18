from django.contrib.auth.models import User,Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from appapprovepermission.models import AppApprove,EmpApprove,EmpApproveDetail
from django.contrib.contenttypes.models import ContentType


class ContentDropdownSerializer(ModelSerializer):

    class Meta:
        model = ContentType
        fields = ['id','app_label','model']


class AppApproveSerializer(ModelSerializer):
    content=ContentDropdownSerializer()

    class Meta:
        model = AppApprove
        fields = ['id','content_id','content','approval_level']


class EmpApproveDetailSerializer(ModelSerializer):
    id = serializers.ModelField(model_field=EmpApproveDetail()._meta.get_field('id'), required=False,
                                allow_null=True)

    class Meta:
        model = EmpApproveDetail
        fields = ['id','emp_approve','emp_level','primary_emp','secondary_emp']


class EmpApproveSerializer(ModelSerializer):
    emp_approve_details=EmpApproveDetailSerializer(many=True)

    class Meta:
        model = EmpApprove
        fields = ['id','content','emp_approve_details']

    def create(self, validated_data):
        emp_approve_details = validated_data.pop('emp_approve_details')
        emp_approve = EmpApprove.objects.create(**validated_data)

        for data in emp_approve_details:
            EmpApproveDetail.objects.create(emp_approve=emp_approve,**data)

        return emp_approve

    def update(self, instance, validated_data):
        emp_approve_details = validated_data.pop('emp_approve_details')
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        for data in emp_approve_details:
                if data['id']:
                    detail = EmpApproveDetail.objects.get(pk=data['id'])

                    detail.emp_level = data.get('emp_level', detail.emp_level)
                    detail.primary_emp = data.get('primary_emp', detail.primary_emp)
                    detail.secondary_emp = data.get('secondary_emp', detail.secondary_emp)
                    detail.save()
        return instance


class EmpApproveDetailReadSerializer(ModelSerializer):
    class Meta:
        model = EmpApproveDetail
        fields = ['id','emp_approve','emp_level','primary_emp_details','secondary_emp_details']


class EmpApproveReadSerializer(ModelSerializer):
    emp_approve_details=EmpApproveDetailReadSerializer(read_only=True,many=True)

    class Meta:
        model = EmpApprove
        fields = ['id','content_details','emp_approve_details']



