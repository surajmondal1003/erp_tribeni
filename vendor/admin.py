from django.contrib import admin
from vendor.models import VendorAccount,VendorAddress,Vendor,VendorType

# Register your models here.
admin.site.register(VendorAccount)
admin.site.register(VendorAddress)
admin.site.register(Vendor)
admin.site.register(VendorType)
