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
    pur_inv=models.ForeignKey(PurchaseInvoice,on_delete=models.SET_NULL,blank=True,null=True)
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


    def company(self):
       companyname= self.pur_inv.grn.po_order.requisition.company.company_name
       company_id= self.pur_inv.grn.po_order.requisition.company.id
       details={'company_name':companyname,'id':company_id}
       return details


    def pur_inv_no(self):
         inv_no=self.pur_inv.purchase_inv_no
         id=self.pur_inv.id
         date=self.pur_inv.created_at
         details = {'inv_no': inv_no, 'id': id,'date':date}
         return details

    def po_order_no(self):
       return self.pur_inv.grn.po_order.purchase_order_no

    def vendor_name(self):
        return self.pur_inv.grn.po_order.vendor.vendor_fullname

    def project_name(self):
        return self.pur_inv.grn.po_order.requisition.project.project_name