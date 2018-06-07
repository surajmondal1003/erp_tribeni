from django.db import models
from purchase_requisition.models import Requisition
from vendor.models import Vendor,VendorAddress
from purchase_order.models import PurchaseOrder
from company.models import Company
from vendor.models import Vendor,VendorAddress
from django.contrib.auth.models import User
from material_master.models import Material
from company_project.models import CompanyProject,CompanyProjectDetail
from uom.models import UOM

# Create your models here.

class GRN(models.Model):

    STATUS_CHOICES = (
        ('2', 'False'),
        ('1', 'True'),
        ('0', 'None'),
    )
    grn_no = models.CharField(max_length=255)#newly added
    po_order=models.ForeignKey(PurchaseOrder,on_delete=models.SET_NULL,blank=True,null=True)
    company=models.ForeignKey(Company,on_delete=models.SET_NULL,blank=True,null=True)
    project = models.ForeignKey(CompanyProject, on_delete=models.SET_NULL, blank=True, null=True)
    vendor=models.ForeignKey(Vendor,on_delete=models.SET_NULL,blank=True,null=True)
    vendor_address=models.ForeignKey(VendorAddress,on_delete=models.SET_NULL,blank=True,null=True)
    waybill_no=models.CharField(max_length=150,blank=True,null=True)#newly added blank=True,null=True
    vehicle_no=models.CharField(max_length=150,blank=True,null=True)#newly added blank=True,null=True
    check_post=models.CharField(max_length=255,blank=True,null=True)#newly added blank=True,null=True
    challan_no=models.CharField(max_length=150)
    challan_date=models.DateTimeField()
    is_approve = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    is_finalised = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def purchase_order_no(self):
        grn= PurchaseOrder.objects.values_list('purchase_order_no',flat=True).filter(id=self.po_order.id)
        return grn.values_list('purchase_order_no')

    def __str__(self):
        return str(self.created_at)



class GRNDetail(models.Model):
    grn=models.ForeignKey(GRN,on_delete=models.CASCADE,related_name='grn_detail')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    uom = models.ForeignKey(UOM, on_delete=models.SET_NULL, blank=True, null=True)
    order_quantity = models.DecimalField(max_digits=20, decimal_places=2)
    receive_quantity = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return str(self.grn.created_at)

class ReversGRN(models.Model):
    STATUS_CHOICES = (
        ('2', 'False'),
        ('1', 'True'),
        ('0', 'None'),
    )
    grn = models.ForeignKey(GRN, on_delete=models.SET_NULL, blank=True, null=True,related_name='reverse_grn')
    revers_gen_no = models.CharField(max_length=255)
    reverse_quantity = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    reverse_reason = models.CharField(max_length=150)
    status = models.BooleanField(default=True)
    is_approve = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    is_finalised = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')


    def __str__(self):
        return str(self.created_at)










