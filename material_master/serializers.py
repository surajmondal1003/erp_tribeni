from material_master.models import MaterialType,Material,Material_UOM,Material_Tax
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from uom.serializers import UOMSerializer

class MaterialTypeSerializer(ModelSerializer):
    material_type = serializers.CharField(validators=[UniqueValidator(queryset=MaterialType.objects.all())])
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    description=serializers.CharField(required=False,allow_null=True,allow_blank=True)

    class Meta:
        model = MaterialType
        fields = ['id','material_type','description','status','created_at','created_by','is_deleted']


class MaterialUOMSerializer(ModelSerializer):
    #base_uom = UOMSerializer()
    #unit_uom = UOMSerializer()
    id = serializers.ModelField(model_field=Material_UOM()._meta.get_field('id'), required=False,
                                allow_null=True)

    class Meta:
        model = Material_UOM
        fields = ['id','material_for','base_uom','unit_per_uom','unit_uom','is_deleted']

class MaterialUOMSerializerforRead(ModelSerializer):
    base_uom = UOMSerializer()
    unit_uom = UOMSerializer()

    class Meta:
        model = Material_UOM
        fields = ['id','material_for','base_uom','unit_per_uom','unit_uom','is_deleted']



class MaterialTaxSerializer(ModelSerializer):
    id = serializers.ModelField(model_field=Material_Tax()._meta.get_field('id'), required=False,
                                allow_null=True)

    class Meta:
        model = Material_Tax
        fields = ['id','tax_for','igst','cgst','sgst','hsn','is_deleted']






class MaterialReadSerializer(ModelSerializer):
    material_type = MaterialTypeSerializer()
    material_uom = serializers.SerializerMethodField()
    material_tax = serializers.SerializerMethodField()


    def get_material_uom(self, obj):
        qs = Material_UOM.objects.filter(material=obj,is_deleted=False)
        serializer = MaterialUOMSerializerforRead(instance=qs,many=True)
        return serializer.data

    def get_material_tax(self, obj):
        qs = Material_Tax.objects.filter(material=obj,is_deleted=False)
        serializer = MaterialTaxSerializer(instance=qs,many=True)
        return serializer.data



    class Meta:
        model = Material
        fields = ['id','material_fullname','material_type','material_code','description','is_taxable','is_sales','status','created_at',
                  'is_deleted','material_uom', 'material_tax','created_by']







class MaterialSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    material_uom = MaterialUOMSerializer(many=True)
    material_tax = MaterialTaxSerializer(many=True)


    class Meta:
        model = Material
        fields = ['id','material_fullname','material_type','material_code','description','is_taxable','is_sales','status','created_at',
                  'is_deleted','material_uom','material_tax','created_by']

    def create(self, validated_data):
        is_taxable = validated_data.get('is_taxable')
        print(is_taxable)

        if is_taxable == True:

            material_uoms = validated_data.pop('material_uom')
            material_taxs = validated_data.pop('material_tax')


            material = Material.objects.create(**validated_data)

            for material_uom in material_uoms:
                Material_UOM.objects.create(material=material, **material_uom)
            for material_tax in material_taxs:
                Material_Tax.objects.create(material=material, **material_tax)


            return material

        else:
            material_uoms = validated_data.pop('material_uom')
            material_taxs = validated_data.pop('material_tax')


            material = Material.objects.create(**validated_data)

            for material_uom in material_uoms:
                Material_UOM.objects.create(material=material, **material_uom)


            return material

    def update(self, instance, validated_data):
                is_taxable = validated_data.get('is_taxable')
                print(is_taxable)

                if is_taxable == True:
                    material_uoms_data = validated_data.pop('material_uom')
                    material_taxs_data = validated_data.pop('material_tax')

                    material_uoms = (instance.material_uom).all()
                    material_uoms = list(material_uoms)
                    material_taxs = (instance.material_tax).all()
                    material_taxs = list(material_taxs)

                    instance.material_fullname = validated_data.get('material_fullname', instance.material_fullname)
                    instance.material_type = validated_data.get('material_type', instance.material_type)
                    instance.material_code = validated_data.get('material_code', instance.material_code)
                    instance.description = validated_data.get('description', instance.description)
                    instance.is_taxable = validated_data.get('is_taxable', instance.is_taxable)
                    instance.is_sales = validated_data.get('is_sales', instance.is_sales)
                    instance.status = validated_data.get('status', instance.status)
                    instance.created_at = validated_data.get('created_at', instance.created_at)
                    instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
                    instance.save()

                    material_uoms_data_ids = list()
                    for material_uoms_data_id in material_uoms_data:
                        if material_uoms_data_id['id']:
                            material_uoms_data_ids.append(material_uoms_data_id['id'])

                    material_uoms_instance_ids = list()
                    for item in material_uoms:
                        material_uoms_instance_ids.append(item.id)

                    uom_updateable_ids = list(set(material_uoms_data_ids) & set(material_uoms_instance_ids))
                    uom_deleteable_ids = list(set(material_uoms_instance_ids) - set(material_uoms_data_ids))

                    for uom_data in material_uoms_data:
                        if uom_data['id'] in uom_updateable_ids:
                            uom = Material_UOM.objects.get(pk=uom_data['id'])

                            uom.material_for = uom_data.get('material_for', uom.material_for)
                            uom.base_uom = uom_data.get('base_uom', uom.base_uom)
                            uom.unit_per_uom = uom_data.get('unit_per_uom', uom.unit_per_uom)
                            uom.unit_uom = uom_data.get('unit_uom', uom.unit_uom)
                            uom.is_deleted = uom_data.get('is_deleted', uom.is_deleted)

                            uom.save()

                        elif uom_data['id'] is None:
                            Material_UOM.objects.create(material=instance, **uom_data)

                    for delete_id in uom_deleteable_ids:
                        uom = Material_UOM.objects.get(pk=delete_id)
                        uom.is_deleted = True
                        uom.save()

                #material tax

                    material_taxs_data_ids = list()
                    for material_taxs_data_id in material_taxs_data:
                        if material_taxs_data_id['id']:
                            material_taxs_data_ids.append(material_taxs_data_id['id'])

                    material_taxs_instance_ids = list()
                    for item in material_taxs:
                        material_taxs_instance_ids.append(item.id)

                    tax_updateable_ids = list(set(material_taxs_data_ids) & set(material_taxs_instance_ids))
                    tax_deleteable_ids = list(set(material_taxs_instance_ids) - set(material_taxs_data_ids))

                    for tax_data in material_taxs_data:
                        if tax_data['id'] in tax_updateable_ids:
                            tax = Material_Tax.objects.get(pk=tax_data['id'])

                            tax.tax_for = tax_data.get('tax_for', tax.tax_for)
                            tax.igst = tax_data.get('igst', tax.igst)
                            tax.cgst = tax_data.get('cgst', tax.cgst)
                            tax.sgst = tax_data.get('sgst', tax.sgst)
                            tax.hsn = tax_data.get('hsn', tax.hsn)
                            tax.is_deleted = tax_data.get('is_deleted', tax.is_deleted)

                            tax.save()

                        elif tax_data['id'] is None:
                            Material_Tax.objects.create(material=instance, **tax_data)

                    for delete_id in tax_deleteable_ids:
                        tax = Material_Tax.objects.get(pk=delete_id)
                        tax.is_deleted = True
                        tax.save()


                    return instance

                else:
                    material_uoms_data = validated_data.pop('material_uom')
                    material_taxs_data = validated_data.pop('material_tax')

                    material_uoms = (instance.material_uom).all()
                    material_uoms = list(material_uoms)
                    material_taxs = (instance.material_tax).all()
                    material_taxs = list(material_taxs)

                    instance.material_fullname = validated_data.get('material_fullname', instance.material_fullname)
                    instance.material_type = validated_data.get('material_type', instance.material_type)
                    instance.material_code = validated_data.get('material_code', instance.material_code)
                    instance.description = validated_data.get('description', instance.description)
                    instance.is_taxable = validated_data.get('is_taxable', instance.is_taxable)
                    instance.is_sales = validated_data.get('is_sales', instance.is_sales)
                    instance.status = validated_data.get('status', instance.status)
                    instance.created_at = validated_data.get('created_at', instance.created_at)
                    instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
                    instance.save()

                    material_uoms_data_ids = list()
                    for material_uoms_data_id in material_uoms_data:
                        if material_uoms_data_id['id']:
                            material_uoms_data_ids.append(material_uoms_data_id['id'])

                    material_uoms_instance_ids = list()
                    for item in material_uoms:
                        material_uoms_instance_ids.append(item.id)

                    uom_updateable_ids = list(set(material_uoms_data_ids) & set(material_uoms_instance_ids))
                    uom_deleteable_ids = list(set(material_uoms_instance_ids) - set(material_uoms_data_ids))

                    for uom_data in material_uoms_data:
                        if uom_data['id'] in uom_updateable_ids:
                            uom = Material_UOM.objects.get(pk=uom_data['id'])

                            uom.material_for = uom_data.get('material_for', uom.material_for)
                            uom.base_uom = uom_data.get('base_uom', uom.base_uom)
                            uom.unit_per_uom = uom_data.get('unit_per_uom', uom.unit_per_uom)
                            uom.unit_uom = uom_data.get('unit_uom', uom.unit_uom)
                            uom.is_deleted = uom_data.get('is_deleted', uom.is_deleted)

                            uom.save()

                        elif uom_data['id'] is None:
                            Material_UOM.objects.create(material=instance, **uom_data)

                    for delete_id in uom_deleteable_ids:
                        uom = Material_UOM.objects.get(pk=delete_id)
                        uom.is_deleted = True
                        uom.save()

                        # material tax

                    material_taxs_data_ids = list()
                    for material_taxs_data_id in material_taxs_data:
                        if material_taxs_data_id['id']:
                            material_taxs_data_ids.append(material_taxs_data_id['id'])

                    material_taxs_instance_ids = list()
                    for item in material_taxs:
                        material_taxs_instance_ids.append(item.id)

                    tax_updateable_ids = list(set(material_taxs_data_ids) & set(material_taxs_instance_ids))
                    tax_deleteable_ids = list(set(material_taxs_instance_ids) - set(material_taxs_data_ids))

                    for tax_data in material_taxs_data:
                        if tax_data['id'] in tax_updateable_ids:
                            tax = Material_Tax.objects.get(pk=tax_data['id'])

                            tax.tax_for = tax_data.get('tax_for', tax.tax_for)
                            tax.igst = tax_data.get('igst', tax.igst)
                            tax.cgst = tax_data.get('cgst', tax.cgst)
                            tax.sgst = tax_data.get('sgst', tax.sgst)
                            tax.hsn = tax_data.get('hsn', tax.hsn)
                            tax.is_deleted = True
                            tax.save()

                        elif tax_data['id'] is None:
                            Material_Tax.objects.create(material=instance, **tax_data)

                    for delete_id in tax_deleteable_ids:
                        tax = Material_Tax.objects.get(pk=delete_id)
                        tax.is_deleted = True
                        tax.save()

                    return instance



class MaterialNameSerializer(ModelSerializer):
    material_tax = MaterialTaxSerializer(many=True)

    class Meta:
        model = Material
        fields = ['id','material_fullname','material_code','material_tax']