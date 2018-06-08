from states.models import State
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

class StateSerializer(ModelSerializer):
    state_name = serializers.CharField(
        validators=[UniqueValidator(queryset=State.objects.all())]
    )

    tin_number = serializers.IntegerField(
        validators=[UniqueValidator(queryset=State.objects.all())]
    )
    state_code=serializers.CharField(
        validators=[UniqueValidator(queryset=State.objects.all())]
    )
    user = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
    status = serializers.BooleanField(default=True)


    class Meta:
        model = State
        fields = ['id','state_name','tin_number','state_code','created_at','user','status','is_deleted']



class StateNameSerializer(ModelSerializer):

    class Meta:
        model = State
        fields = ['id','state_name']