from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from vendor.models import VendorType,Vendor,VendorAccount,VendorAddress

class VendorTypeSerializer(ModelSerializer):
    vendor_type = serializers.CharField(validators=[UniqueValidator(queryset=VendorType.objects.all())])
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)


    class Meta:
        model = VendorType
        fields = ['id','vendor_type','status','created_at','created_by','is_deleted']


class VendorAddressSerializer(ModelSerializer):
    designation=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    id = serializers.ModelField(model_field=VendorAddress()._meta.get_field('id'), required=False, allow_null=True)


    class Meta:
        model = VendorAddress
        fields = ['id','address','state','city','pincode','mobile','email','designation','contact_person','is_deleted']
        # fields = ['id', 'address', 'state', 'city', 'pincode', 'mobile', 'email', 'designation', 'contact_person']


class VendorAccountSerializer(ModelSerializer):
    id = serializers.ModelField(model_field=VendorAccount()._meta.get_field('id'), required=False, allow_null=True)
    class Meta:
        model = VendorAccount
        fields = ['id', 'bank_name', 'branch_name', 'account_no', 'ifsc_code','is_deleted']




# class VendorSerializer(ModelSerializer):
#
#     created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     status = serializers.BooleanField(default=True)
#     vendor_address = VendorAddressSerializer(many=True)
#     vendor_account = VendorAccountSerializer(many=True)
#
#
#     class Meta:
#         model = Vendor
#         fields = ['id','vendor_fullname','vendor_type','company','pan_no','gst_no','cin_no','status','created_at','created_by'
#                   ,'is_deleted','vendor_address','vendor_account']
#
#     def create(self, validated_data):
#
#             vendor_address_data = validated_data.pop('vendor_address')
#             vendor_account_data = validated_data.pop('vendor_account')
#
#
#             vendor = Vendor.objects.create(**validated_data)
#
#             for vendor_address in vendor_address_data:
#                 VendorAddress.objects.create(vendor=vendor, **vendor_address)
#             for vendor_account in vendor_account_data:
#                 VendorAccount.objects.create(vendor=vendor, **vendor_account)
#
#
#             return vendor
#
#     def update(self, instance, validated_data):
#
#             vendor_address_data = validated_data.pop('vendor_address')
#             vendor_account_data = validated_data.pop('vendor_account')
#
#             vendor_addresses = (instance.vendor_address).all()
#             vendor_addresses = list(vendor_addresses)
#             vendor_accounts = (instance.vendor_account).all()
#             vendor_accounts = list(vendor_accounts)
#
#
#             # print(vendor_addresses)
#             # print(vendor_address_data)
#
#             instance.vendor_fullname = validated_data.get('vendor_fullname', instance.vendor_fullname)
#             instance.vendor_type = validated_data.get('vendor_type', instance.vendor_type)
#             instance.company = validated_data.get('company', instance.company)
#             instance.pan_no = validated_data.get('pan_no', instance.pan_no)
#             instance.gst_no = validated_data.get('gst_no', instance.gst_no)
#             instance.cin_no = validated_data.get('cin_no', instance.cin_no)
#             instance.status = validated_data.get('status', instance.status)
#             instance.created_at = validated_data.get('created_at', instance.created_at)
#             instance.created_by = validated_data.get('created_by', instance.created_by)
#             instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
#             instance.save()
#
#
#             for vendor_address in vendor_addresses:
#                 if vendor_address:
#                     vendor_address.delete()
#             for vendor_account in vendor_accounts:
#                 if vendor_account:
#                     vendor_account.delete()
#
#
#             for vendor_address in vendor_address_data:
#                 VendorAddress.objects.create(vendor=instance, **vendor_address)
#             for vendor_account in vendor_account_data:
#                 VendorAccount.objects.create(vendor=instance, **vendor_account)
#
#
#             return instance




class VendorSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    vendor_address = VendorAddressSerializer(many=True)
    vendor_account = VendorAccountSerializer(many=True)


    class Meta:
        model = Vendor
        fields = ['id','vendor_fullname','vendor_type','company','pan_no','gst_no','cin_no','status','created_at','created_by'
                  ,'is_deleted','vendor_address','vendor_account']

    def create(self, validated_data):

            vendor_address_data = validated_data.pop('vendor_address')
            vendor_account_data = validated_data.pop('vendor_account')


            vendor = Vendor.objects.create(**validated_data)

            for vendor_address in vendor_address_data:
                VendorAddress.objects.create(vendor=vendor, **vendor_address)
            for vendor_account in vendor_account_data:
                VendorAccount.objects.create(vendor=vendor, **vendor_account)


            return vendor

    def update(self, instance, validated_data):

            vendor_address_data = validated_data.pop('vendor_address')
            vendor_account_data = validated_data.pop('vendor_account')

            vendor_addresses = (instance.vendor_address).all()
            vendor_addresses = list(vendor_addresses)
            vendor_accounts = (instance.vendor_account).all()
            vendor_accounts = list(vendor_accounts)



            instance.vendor_fullname = validated_data.get('vendor_fullname', instance.vendor_fullname)
            instance.vendor_type = validated_data.get('vendor_type', instance.vendor_type)
            instance.company = validated_data.get('company', instance.company)
            instance.pan_no = validated_data.get('pan_no', instance.pan_no)
            instance.gst_no = validated_data.get('gst_no', instance.gst_no)
            instance.cin_no = validated_data.get('cin_no', instance.cin_no)
            instance.status = validated_data.get('status', instance.status)
            instance.created_at = validated_data.get('created_at', instance.created_at)
            instance.created_by = validated_data.get('created_by', instance.created_by)
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.save()


            #multipledata(instance,vendor_address_data,vendor_addresses,VendorAddress,VendorAddressSerializer)


            vendor_addresses_ids=list()
            for vendor_address_id in vendor_address_data:
                if vendor_address_id['id']:
                    vendor_addresses_ids.append(vendor_address_id['id'])

            vendor_addresses_instance_ids=list()
            for item in vendor_addresses:
                vendor_addresses_instance_ids.append(item.id)

            updateable_ids = list(set(vendor_addresses_ids) & set(vendor_addresses_instance_ids))
            deleteable_ids = list(set(vendor_addresses_instance_ids) - set(vendor_addresses_ids))



            for address_data in vendor_address_data:
                if address_data['id'] in updateable_ids:
                    address = VendorAddress.objects.get(pk=address_data['id'])

                    address.address=address_data.get('address', address.address)
                    address.state=address_data.get('state', address.state)
                    address.city=address_data.get('city', address.city)
                    address.pincode=address_data.get('pincode', address.pincode)
                    address.mobile=address_data.get('mobile', address.mobile)
                    address.email=address_data.get('email', address.email)
                    address.designation=address_data.get('designation', address.designation)
                    address.contact_person=address_data.get('contact_person', address.contact_person)
                    address.is_deleted=address_data.get('is_deleted', address.is_deleted)
                    address.save()

                elif address_data['id'] is None:
                    VendorAddress.objects.create(vendor=instance, **address_data)

            for delete_id in deleteable_ids:
                address = VendorAddress.objects.get(pk=delete_id)
                address.is_deleted = True
                address.save()


            vendor_accounts_ids = list()
            for vendor_account_id in vendor_account_data:
                if vendor_account_id['id']:
                    vendor_accounts_ids.append(vendor_account_id['id'])

            vendor_accounts_instance_ids = list()
            for item in vendor_accounts:
                vendor_accounts_instance_ids.append(item.id)

            account_updateable_ids = list(set(vendor_accounts_ids) & set(vendor_accounts_instance_ids))
            account_deleteable_ids = list(set(vendor_accounts_instance_ids) - set(vendor_accounts_ids))



            for account_data in vendor_account_data:
                if account_data['id'] in account_updateable_ids:
                    account = VendorAccount.objects.get(pk=account_data['id'])

                    account.bank_name = account_data.get('bank_name', account.bank_name)
                    account.branch_name = account_data.get('branch_name', account.branch_name)
                    account.account_no = account_data.get('account_no', account.account_no)
                    account.ifsc_code = account_data.get('ifsc_code', account.ifsc_code)
                    account.is_deleted = account_data.get('is_deleted', account.is_deleted)
                    account.save()

                elif account_data['id'] is None:
                    VendorAccount.objects.create(vendor=instance, **account_data)

            for delete_id in account_deleteable_ids:
                account = VendorAccount.objects.get(pk=delete_id)
                account.is_deleted = True
                account.save()

            return instance






def multipledata(object,request_data,object_data,modelname,serializer_name):
    request_data_ids = list()
    for item_id in request_data:
        if item_id['id']:
            request_data_ids.append(item_id['id'])

    object_ids = list()
    for item in object_data:
        object_ids.append(item.id)

    updateable_ids = list(set(request_data_ids) & set(object_ids))
    deleteable_ids = list(set(object_ids) - set(request_data_ids))

    #print(modelname)
    for item_data in request_data:
            if item_data['id'] in updateable_ids:
                item_instance = modelname.objects.filter(pk=item_data['id'])

                for i in request_data[0].keys():
                    item_data_ins = "item_instance.{}=item_instance.get({},item_instance.{})". format(i,item_data[i],i)
                    print(type(serializer_name))
                    #item_instance=(item_data_ins).save()
                    item_serializer=serializer_name(data=item_data_ins)
                    #print(item_serializer)
                    if item_serializer.is_valid():
                        print('update')
                        item_serializer.save()


class VendorNameSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id','vendor_fullname']




class VendorUpdateStatusSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id','status','is_deleted']


    def update(self, instance, validated_data):
            instance.status = validated_data.get('status', instance.status)
            instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
            instance.save()

            return instance




class VendorReadSerializer(ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.BooleanField(default=True)
    vendor_address = serializers.SerializerMethodField()
    vendor_account = serializers.SerializerMethodField()

    def get_vendor_address(self, obj):
        qs = VendorAddress.objects.filter(vendor=obj,is_deleted=False)
        serializer = VendorAddressSerializer(instance=qs,many=True)
        return serializer.data

    def get_vendor_account(self,obj):
        qs = VendorAccount.objects.filter(vendor=obj,is_deleted=False)
        serializer = VendorAccountSerializer(instance=qs,many=True)
        return serializer.data


    class Meta:
        model = Vendor
        fields = ['id','vendor_fullname','vendor_type','company','pan_no','gst_no','cin_no','status','created_at','created_by'
                  ,'is_deleted','vendor_address','vendor_account']

