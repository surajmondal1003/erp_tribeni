from django.contrib.auth.models import User,Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from authentication.models import EmployeeProfile
from attendance.models import Attendance


class AttendanceSerializer(ModelSerializer):

    class Meta:
        model = Attendance
        fields = ['id','employee','in_time','out_time','date','is_deleted']