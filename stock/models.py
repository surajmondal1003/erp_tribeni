from django.db import models
from django.contrib.auth.models import User
from company.models import Company
# from purchase_invoice.serializers import PurchaseInvoice,PurchaseInvoiceMap
from grn.models import GRN,GRNDetail
from material_master.models import Material,MaterialType
from company_project.models import CompanyProject,CompanyProjectDetail
from uom.models import UOM
from material_master.models import Material_UOM
from contractor.models import Contractor
# Create your models here.

class Stock(models.Model):
    grn = models.ForeignKey(GRN, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    company_project = models.ForeignKey(CompanyProject, on_delete=models.SET_NULL, blank=True, null=True)
    material_type = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at)

    def grn_number(self):
        return self.grn.grn_no

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


class StockView(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    company_project = models.ForeignKey(CompanyProject, on_delete=models.SET_NULL, blank=True, null=True)
    material_type = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    avl_qty = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company_project.project_name)

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
    def company_details(self):
        id=self.company.id
        name=self.company.company_name
        details = {'id': id, 'name': name}
        return details

    def company_project_details(self):
        id=self.company_project.id
        project_name = self.company_project.project_name
        details = {'id': id, 'project_name': project_name}
        return details

    def material_details(self):
        id = self.material.id
        material_fullname = self.material.material_fullname
        material_code = self.material.material_code
        details = {'id': id, 'material_fullname': material_fullname,'material_code':material_code}
        return details

class StockIssue(models.Model):
    ISSUETYPE_CHOICES = (
        ('2', 'OnProject'),
        ('1', 'OutProject'),
        ('0', 'None'),

    )
    TRANSFER_TYPE=(
        ('3', 'Freeable'),
        ('2', 'Chargeable'),
        ('1', 'Returnable'),
        ('0', 'None'),
    )

    stockview = models.ForeignKey(StockView, on_delete=models.SET_NULL, blank=True, null=True)
    from_project = models.ForeignKey(CompanyProject, on_delete=models.SET_NULL, blank=True, null=True,related_name='from_project')
    to_project = models.ForeignKey(CompanyProject, on_delete=models.SET_NULL, blank=True, null=True,related_name='to_project')
    issue_type = models.CharField(max_length=1, choices=ISSUETYPE_CHOICES, default='0')
    transfer_type = models.CharField(max_length=1, choices=TRANSFER_TYPE, default='0')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created_at)


class StockTransfer(models.Model):
        stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, blank=True, null=True)
        quantity = models.DecimalField(max_digits=10, decimal_places=2)
        note = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
        status = models.BooleanField(default=True)
        is_deleted = models.BooleanField(default=False)

        def __str__(self):
            return str(self.created_at)

