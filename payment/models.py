from django.db import models
from vendor.models import Vendor,VendorAddress
from django.contrib.auth.models import User
from purchase_invoice.serializers import PurchaseInvoice
from company.models import Company
from banks.models import Bank
from purchase_order.models import PurchaseOrder
from company_project.models import CompanyProject
# Create your models here.

class Payment(models.Model):
    STATUS_CHOICES = (
        ('2', 'False'),
        ('1', 'True'),
        ('0', 'None'),
    )

    payment_no = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    project = models.ForeignKey(CompanyProject, on_delete=models.SET_NULL, blank=True, null=True)
    pur_inv=models.ForeignKey(PurchaseInvoice,on_delete=models.SET_NULL,blank=True,null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    vendor_address = models.ForeignKey(VendorAddress, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_inv_no = models.CharField(max_length=255)
    purchase_inv_date = models.DateTimeField(blank=True,null=True)
    po_order=models.ForeignKey(PurchaseOrder,on_delete=models.SET_NULL,blank=True,null=True)
    po_order_no=models.CharField(max_length=255,blank=True,null=True)
    bank=models.ForeignKey(Bank,on_delete=models.SET_NULL,blank=True,null=True)
    payment_mode = models.CharField(max_length=255,blank=True,null=True)
    payment_refrence = models.CharField(max_length=255,blank=True,null=True)
    total_amount=models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    special_note=models.TextField(blank=True,null=True)
    is_approve = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    is_paid=models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at)



