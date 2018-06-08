from stock.models import Stock,StockIssue
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from company.serializers import CompanyListSerializer
from authentication.serializers import UserLoginSerializer,UserReadSerializer
from material_master.serializers import MaterialNameSerializer,MaterialReadSerializer,MaterialSerializer
from company_project.serializers import CompanyProjectSerializer, CompanyProjectDetailsSerializer
from material_master.serializers import MaterialTypeSerializer
from grn.serializers import *
from uom.serializers import *

class StockSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    queryset = Stock.objects.all()
    class Meta:
        model = Stock
        fields = ['id','grn','company','company_project','material_type','material','rate','quantity','uom','created_at','created_by','status']

    def create(self, validated_data):

        stock = Stock.objects.create(**validated_data)

        return stock

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity',instance.quantity)
        instance.save()

        return instance



class StockReadSerializer(ModelSerializer):

    #created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    grn = GRNSerializer(read_only=True)
    company = CompanyListSerializer(read_only=True)
    company_project = CompanyProjectSerializer(read_only=True)
    material_type = MaterialTypeSerializer(read_only=True)
    material = MaterialNameSerializer(read_only=True)
    status = serializers.BooleanField(default=True)
    uom =UOMSerializer(read_only=True)



    class Meta:
        model = Stock
        fields = ['id','grn','company','company_project','material_type','material','rate','quantity','uom','created_at','status']


class StockIssueSerializer(ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = StockIssue
        fields = ['id','stock','quantity','note','status','created_at','created_by']



class StockIssueReadSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = StockIssue
        fields = ['id','stock_id','quantity', 'note','created_at','created_by','status']


