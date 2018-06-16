from django.contrib.auth.models import User,Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from authentication.models import EmployeeProfile



class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',

        ]


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',


        ]


class EmployeeProfileSerializer(ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    blood_group=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    alt_contact=serializers.CharField(required=False,allow_blank=True,allow_null=True)
    pan=serializers.CharField(required=False,allow_blank=True,allow_null=True)


    class Meta:
        model = EmployeeProfile
        fields = ['id','user','company','departments','designation','contact','dob','alt_contact',
                  'pan','blood_group','adhaar_no','emp_present_address','emp_present_state','emp_present_city','emp_present_pin',
                  'emp_permanent_address','emp_permanent_state','emp_permanent_city','emp_permanent_pin','created_at','status'
                  ,'is_deleted','created_by']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    employee_profile_details=EmployeeProfileSerializer(many=True)

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email','groups','employee_profile_details']

    def create(self, validated_data):
        employee_profile_details = validated_data.pop('employee_profile_details')

        validated_data['username']=validated_data['email']
        validated_data['password']='123456'

        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])

        user.set_password(validated_data['password'])
        user.first_name=validated_data['first_name']
        user.last_name=validated_data['last_name']
        user.save()

        group_id=0
        if validated_data['groups']:
            for i in validated_data['groups']:
                group_id=i.id
            group = Group.objects.get(id=group_id)
            group.user_set.add(user)

        for profile_details in employee_profile_details:
            EmployeeProfile.objects.create(user=user,first_name=user.first_name,last_name=user.last_name,
                                           email=user.email,**profile_details)

        return user


class EmployeeReadSerializer(ModelSerializer):

    class Meta:
        model = EmployeeProfile
        fields = ['id','user','company_details','department_details','designation_details','first_name','last_name','email','contact','dob','alt_contact',
                  'pan','blood_group','adhaar_no','emp_present_address','emp_present_state','emp_present_city','emp_present_pin',
                  'emp_permanent_address','emp_permanent_state','emp_permanent_city','emp_permanent_pin','created_at','status',
                  'is_deleted','created_by_details']
