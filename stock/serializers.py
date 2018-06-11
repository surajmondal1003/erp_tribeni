from stock.models import Stock,StockIssue,StockView
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


class StockListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        stocks = [Stock(**item) for item in validated_data]
        return Stock.objects.bulk_create(stocks)


class StockSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    queryset = Stock.objects.all()
    class Meta:
        model = Stock
        fields = ['id','grn','company','company_project','material_type','material','rate','quantity','created_at','created_by',
                  'status','is_deleted']
    # def __init__(self,*args, **kwargs):
    #     many = kwargs.pop('many', True)
    #     super(StockSerializer, self).__init__(many=many, *args, **kwargs)

    def create(self, validated_data):
        stock = Stock.objects.create(**validated_data)
        stockview=StockView.objects.filter(company=stock.company,company_project=stock.company_project,material=stock.material)
        if stockview:
            sum=0
            for i in stockview:
                i.material_type=i.material_type
                i.material=i.material
                i.company=i.company
                i.avl_qty += stock.quantity

                sum += i.rate
                avg = sum / len(stockview)
                print(avg)
                i.save()
        else:
            StockView.objects.create(company=stock.company,company_project=stock.company_project,material=stock.material,
                                     avl_qty=stock.quantity,material_type=stock.material_type,rate=stock.rate)
        return stock


    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity',instance.quantity)
        instance.save()

        return instance


# class StockSerializer(serializers.Serializer):
#
#     created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     status = serializers.BooleanField(default=True)
#     queryset = Stock.objects.all()
#     class Meta:
#         list_serializer_class=StockListSerializer(many=True)
#         fields = ['id','grn','company','company_project','material_type','material','rate','quantity','created_at','created_by',
#                   'status','is_deleted']




class StockReadSerializer(ModelSerializer):
    grn = GRNSerializer(read_only=True)
    company = CompanyListSerializer(read_only=True)
    company_project = CompanyProjectSerializer(read_only=True)
    material_type = MaterialTypeSerializer(read_only=True)
    material = MaterialNameSerializer(read_only=True)
    status = serializers.BooleanField(default=True)

    class Meta:
        model = Stock
        fields = ['id','grn','company','company_project','material_type','material','rate','quantity','created_at','status','is_deleted',
                  'grn_number','material_uom']


class StockIssueSerializer(ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = StockIssue
        fields = ['id','from_project','to_project','stockview','issue_type','transfer_type','quantity','note','contractor','status','created_at','created_by']

    def create(self, validated_data):

        stockissue = StockIssue.objects.create(**validated_data)
        print(stockissue.stockview.id)
        stock_view = StockView.objects.filter(id=stockissue.stockview.id)
        for i in stock_view:
            i.avl_qty = i.avl_qty - stockissue.quantity
            i.save()

        if stockissue.from_project != stockissue.to_project:
            StockView.objects.create(company=stockissue.to_project.company, company_project=stockissue.to_project,
                                     material=stockissue.stockview.material,
                                     avl_qty=stockissue.quantity, material_type=stockissue.stockview.material_type,
                                     rate=stockissue.stockview.rate)

        return stockissue



class StockIssueReadSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)

    class Meta:
        model = StockIssue
        fields = ['id','stockview','quantity', 'note','created_at','created_by','status']



class StockViewReadSerializer(ModelSerializer):

    #created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # grn = GRNSerializer(read_only=True)
    # company = CompanyListSerializer(read_only=True)
    # company_project = CompanyProjectSerializer(read_only=True)
    material_type = MaterialTypeSerializer(read_only=True)
    # material = MaterialNameSerializer(read_only=True)
    # status = serializers.BooleanField(default=True)

    class Meta:
        model = StockView
        fields = ['id','company_details','company_project_details','material_type','material_details','rate','avl_qty','status','is_deleted'
                  ,'material_uom']


