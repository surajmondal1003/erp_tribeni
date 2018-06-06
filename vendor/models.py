from django.db import models
from django.contrib.auth.models import User
from company.models import Company
from states.models import State






class VendorType(models.Model):
    vendor_type=models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.vendor_type)


class Vendor(models.Model):
    vendor_fullname=models.CharField(max_length=100)
    vendor_type=models.ForeignKey(VendorType,on_delete=models.SET_NULL,blank=True,null=True)
    company=models.ForeignKey(Company,on_delete=models.SET_NULL,blank=True,null=True)
    pan_no=models.CharField(max_length=255,blank=True,null=True)
    gst_no=models.CharField(max_length=255,blank=True,null=True)
    cin_no=models.CharField(max_length=255,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.vendor_fullname)


class VendorAddress(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE,related_name='vendor_address')
    address=models.TextField()
    state=models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True)
    city=models.CharField(max_length=255)
    pincode=models.CharField(max_length=255)
    mobile=models.BigIntegerField()
    email=models.EmailField(max_length=255,blank=True,null=True)
    designation=models.CharField(max_length=255,blank=True,null=True)
    contact_person=models.CharField(max_length=255,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return str(self.vendor.vendor_fullname)



class VendorAccount(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name='vendor_account')
    bank_name=models.CharField(max_length=255)
    branch_name=models.CharField(max_length=255)
    account_no=models.CharField(max_length=255)
    ifsc_code=models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return str(self.vendor.vendor_fullname)