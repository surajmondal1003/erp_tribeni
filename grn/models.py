from django.db import models
from purchase_requisition.models import Requisition
from vendor.models import Vendor,VendorAddress
from purchase_order.models import PurchaseOrder
from company.models import Company
from vendor.models import Vendor,VendorAddress
from django.contrib.auth.models import User
from material_master.models import Material,Material_UOM
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
    approval_level = models.IntegerField(default='0')

    def purchase_order_no(self):
        return self.po_order.purchase_order_no

    def __str__(self):
        return str(self.created_at)

    def project(self):
        name=self.po_order.requisition.project.project_name
        id=self.po_order.requisition.project.id
        details = {'id': id, 'name': name}
        return details



class GRNDetail(models.Model):
    grn=models.ForeignKey(GRN,on_delete=models.CASCADE,related_name='grn_detail')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    order_quantity = models.DecimalField(max_digits=20, decimal_places=2)
    receive_quantity = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return str(self.grn.created_at)

    def material_uom(self):
        uom=Material_UOM.objects.values_list('base_uom').filter(material=self.material,material_for='1')
        #print(uom.values_list('base_uom')[0])
        materialuom=0
        for i in uom:
            if i[0]:
                materialuom=i[0]
        uom_name=UOM.objects.filter(id=materialuom)
        name=''
        for j in uom_name:
            name=j.name
        return name


class ReversGRN(models.Model):
    STATUS_CHOICES = (
        ('2', 'False'),
        ('1', 'True'),
        ('0', 'None'),
    )
    grn = models.ForeignKey(GRN, on_delete=models.SET_NULL, blank=True, null=True,related_name='reverse_grn')
    revers_gen_no = models.CharField(max_length=255)
    #reverse_quantity = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_approve = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    is_finalised = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    approval_level = models.IntegerField(default='0')


    def __str__(self):
        return str(self.created_at)



class ReverseGRNDetail(models.Model):
    reverse_grn=models.ForeignKey(ReversGRN,on_delete=models.CASCADE,related_name='reverse_grn_detail')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    reverse_grn_quantity = models.DecimalField(max_digits=20, decimal_places=2)
    reverse_reason = models.CharField(max_length=150,blank=True,null=True)

    def __str__(self):
        return str(self.reverse_grn)

    def material_details(self):
        id=self.material.id
        name=self.material.name
        details={'id':id,'name':name}
        return details








