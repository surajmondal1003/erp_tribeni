from django.db import models
from django.contrib.auth.models import User
from grn.models import GRN,GRNDetail
from purchase_order.models import PurchaseOrder
from vendor.models import Vendor,VendorAddress
from company.models import Company
from material_master.models import Material

# Create your models here.


class PurchaseInvoice(models.Model):
    STATUS_CHOICES = (
        ('2', 'False'),
        ('1', 'True'),
        ('0', 'None'),
    )

    purchase_inv_no = models.CharField(max_length=255)
    grn=models.ForeignKey(GRN,on_delete=models.SET_NULL,blank=True,null=True)
    total_gst=models.DecimalField(max_digits=20,decimal_places=2)
    total_amount=models.DecimalField(max_digits=20,decimal_places=2)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    vendor_address = models.ForeignKey(VendorAddress, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    is_approve = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    is_finalised = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    approval_level = models.IntegerField(default='0')

    def __str__(self):
        return str(self.created_at)


    def grn_number(self):
        return self.grn.grn_no

    def po_order_no(self):
        return self.grn.po_order.purchase_order_no

    def project_name(self):
        return self.grn.po_order.requisition.project.project_name

    # def grn_material(self):
    #     return GRNDetail.objects.filter(grn=self.grn)



class PurchaseInvoiceDetail(models.Model):
    pur_invoice=models.ForeignKey(PurchaseInvoice,on_delete=models.CASCADE,related_name='pur_invoice_detail')
    material=models.ForeignKey(Material,on_delete=models.SET_NULL,blank=True,null=True)
    rate=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.DecimalField(max_digits=10,decimal_places=2)
    discount_per=models.DecimalField(max_digits=10,decimal_places=2)
    discount_amount=models.DecimalField(max_digits=10,decimal_places=2)
    igst=models.DecimalField(max_digits=10,decimal_places=2)
    cgst=models.DecimalField(max_digits=10,decimal_places=2)
    sgst=models.DecimalField(max_digits=10,decimal_places=2)
    total_gst=models.DecimalField(max_digits=10,decimal_places=2)
    material_value=models.DecimalField(max_digits=10,decimal_places=2)
    material_amount_pay=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return str(self.pur_invoice.created_at)



