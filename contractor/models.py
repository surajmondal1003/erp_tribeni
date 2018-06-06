from django.db import models
from django.contrib.auth.models import User
from company.models import Company
from states.models import State

# Create your models here.


class Contractor(models.Model):
    contractor_name=models.CharField(max_length=100)
    pan_no=models.CharField(max_length=255,blank=True,null=True)
    gst_no=models.CharField(max_length=255,blank=True,null=True)
    address = models.TextField()
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255)
    mobile = models.BigIntegerField()
    email = models.EmailField(max_length=255,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return str(self.contractor_name)




class ContractorAccount(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE,related_name='contractor_account')
    bank_name=models.CharField(max_length=255)
    branch_name=models.CharField(max_length=255)
    account_no=models.CharField(max_length=255)
    ifsc_code=models.CharField(max_length=255)


    def __str__(self):
        return str(self.contractor.contractor_name)



