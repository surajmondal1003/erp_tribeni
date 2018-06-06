from departments.models import Departments
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from company.serializers import CompanyListSerializer
from authentication.serializers import UserLoginSerializer,UserReadSerializer

class DepartmentsSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    queryset = Departments.objects.all()
    class Meta:
        model = Departments
        fields = ['id','company','department_name','created_at','created_by','status','is_deleted']

    def create(self, validated_data):
        departments = Departments.objects.create(**validated_data)
        return departments

    def update(self, instance, validated_data):
        instance.company = validated_data.get('company', instance.status)
        instance.department_name = validated_data.get('department_name', instance.status)
        instance.status = validated_data.get('status', instance.status)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()
        return instance


class DepartmentsReadSerializer(ModelSerializer):

    created_by = UserReadSerializer()
    company = CompanyListSerializer()

    status = serializers.BooleanField(default=True)

    class Meta:
        model = Departments
        fields = ['id','company','department_name','created_at','created_by','status','is_deleted']


class  DepartmentsListSerializer(ModelSerializer):
    class Meta:
        model =  Departments
        fields = ['id','department_name']


class DepartmentUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = Departments
        fields = ['id','status','is_deleted']


    def update(self, instance, validated_data):
            instance.status = validated_data.get('status', instance.status)
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.save()

            return instance
