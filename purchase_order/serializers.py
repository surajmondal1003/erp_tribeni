from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from uom.serializers import UOMSerializer
import datetime
from purchase_order.models import PurchaseOrderTerms,PurchaseOrderFreight,PurchaseOrderDetail,PurchaseOrder
from material_master.serializers import MaterialNameSerializer
from company.serializers import CompanyListSerializer,TermsAndConditionSerializer
from authentication.serializers import UserReadSerializer
from company_project.serializers import CompanyProjectSerializer,CompanyProjectDetailsSerializer
from rest_framework.relations import StringRelatedField
from vendor.serializers import VendorAddressSerializer,VendorNameSerializer
from purchase_requisition.models import Requisition,RequisitionDetail
from purchase_requisition.serializers import RequisitionProjectNameSerializer




class PurchaseTermsSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrderTerms
        fields = ['id','po_terms']


class PurchaseFreightSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrderFreight
        fields = ['id','freight_option','vendor','freight_rate','freight_amount','freight_gst_rate','freight_total']



class PurchaseDetailSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrderDetail
        fields = ['id','material','uom','requisition_quantity',
                  'order_quantity', 'rate', 'material_value', 'discount_percent', 'discount_value', 'igst',
                  'cgst','sgst', 'gst_amount', 'sub_total', 'delivery_date']




class PurchaseOrderSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    purchase_order_detail = PurchaseDetailSerializer(many=True)
    purchase_order_freight = PurchaseFreightSerializer(many=True)
    purchase_order_terms = PurchaseTermsSerializer(many=True)


    class Meta:
        model = PurchaseOrder
        fields = ['id','requisition','quotation_no','quotation_date','company','vendor','vendor_address',
                  'grand_total','grand_total_words','is_approve','is_finalised','status','created_at','created_by',
                  'purchase_order_detail','purchase_order_freight','purchase_order_terms']



    def create(self, validated_data):

        purchase_order_detail_data = validated_data.pop('purchase_order_detail')
        purchase_order_freight_data = validated_data.pop('purchase_order_freight')
        purchase_order_terms_data = validated_data.pop('purchase_order_terms')


        po_order = PurchaseOrder.objects.create(**validated_data)

        purchase_order_no = str(datetime.date.today()) + '/O-00' + str(po_order.id)

        for purchase_order_detail in purchase_order_detail_data:
            detail=PurchaseOrderDetail.objects.create(po_order=po_order, **purchase_order_detail)
            detail.avail_qty=detail.order_quantity
            detail.save()

            requisition=RequisitionDetail.objects.filter(requisition=detail.po_order.requisition,material=detail.material)
            for i in requisition:
                i.avail_qty=i.avail_qty - detail.order_quantity
                i.save()

        for purchase_order_freight in purchase_order_freight_data:
            PurchaseOrderFreight.objects.create(po_order=po_order, **purchase_order_freight)
        for purchase_order_terms in purchase_order_terms_data:
            PurchaseOrderTerms.objects.create(po_order=po_order, **purchase_order_terms)

        po_order.purchase_order_no = purchase_order_no
        po_order.save()


        return po_order


    def update(self, instance, validated_data):
            purchase_order_detail_data = validated_data.pop('purchase_order_detail')
            purchase_order_freight_data = validated_data.pop('purchase_order_freight')
            purchase_order_terms_data = validated_data.pop('purchase_order_terms')

            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)

            instance.save()

            return instance




class PurchaseDetailReadSerializer(ModelSerializer):

    material=MaterialNameSerializer(read_only=True)
    uom=UOMSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderDetail
        fields = ['id','material','uom','requisition_quantity',
                  'order_quantity', 'rate', 'material_value', 'discount_percent', 'discount_value', 'igst',
                  'cgst','sgst', 'gst_amount', 'sub_total', 'delivery_date','avail_qty']



class PurchseTermsReadSerializer(ModelSerializer):
    po_terms=TermsAndConditionSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderTerms
        fields = ['id','po_terms']


class PurchaseOrderReadSerializer(ModelSerializer):
    company=CompanyListSerializer()
    created_by=UserReadSerializer()
    purchase_order_detail = PurchaseDetailReadSerializer(many=True)
    purchase_order_freight = PurchaseFreightSerializer(many=True)
    purchase_order_terms = PurchseTermsReadSerializer(many=True)
    vendor=VendorNameSerializer(read_only=True)
    vendor_address=VendorAddressSerializer(read_only=True)
    requisition=RequisitionProjectNameSerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id','quotation_no','quotation_date','company','vendor','vendor_address',
                  'grand_total','grand_total_words','is_approve','is_finalised','status','created_at','created_by',
                  'purchase_order_detail','purchase_order_freight','purchase_order_terms','purchase_order_no','requisition']


class PurchaseDetailReadForGRNSerializer(ModelSerializer):
    material=MaterialNameSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderDetail
        fields = ['id','material','uom','requisition_quantity',
                  'order_quantity', 'rate', 'material_value', 'discount_percent', 'discount_value', 'igst',
                  'cgst','sgst', 'gst_amount', 'sub_total', 'delivery_date','avail_qty']



class PurchaseOrderReadForGRNSerializer(ModelSerializer):

    purchase_order_detail = PurchaseDetailReadSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = ['id','purchase_order_detail']

class PurchaseOrderUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['id','status','is_approve','is_finalised']


    def update(self, instance, validated_data):
            instance.is_approve = validated_data.get('is_approve', instance.is_approve)
            instance.is_finalised = validated_data.get('is_finalised', instance.is_finalised)
            instance.status = validated_data.get('status', instance.status)
            instance.save()

            return instance