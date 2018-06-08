from django.db import models
from django.contrib.auth.models import User
from company.models import Company
# from purchase_invoice.serializers import PurchaseInvoice,PurchaseInvoiceMap
from grn.models import GRN,GRNDetail
from material_master.models import Material,MaterialType
from company_project.models import CompanyProject,CompanyProjectDetail
from uom.models import UOM
# Create your models here.

class Stock(models.Model):
    grn = models.ForeignKey(GRN, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    company_project = models.ForeignKey(CompanyProject, on_delete=models.SET_NULL, blank=True, null=True)
    material_type = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    uom = models.ForeignKey(UOM, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.created_at)


class StockIssue(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.created_at)

class StockTransfer(models.Model):
        stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, blank=True, null=True)
        quantity = models.DecimalField(max_digits=10, decimal_places=2)
        note = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
        status = models.BooleanField(default=True)

        def __str__(self):
            return str(self.created_at)

