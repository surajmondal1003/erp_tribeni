from django.db import models
from company.models import Company
from django.contrib.auth.models import User
from material_master.models import Material,MaterialType
from company_project.models import CompanyProject,CompanyProjectDetail
from uom.models import UOM


# Create your models here.

class Requisition(models.Model):
    STATUS_CHOICES = (
        ('2', 'False'),
        ('1', 'True'),
        ('0', 'None'),
    )

    requisition_no = models.CharField(max_length=255)
    company=models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True,related_name='requisition_company')
    project=models.ForeignKey(CompanyProject, on_delete=models.SET_NULL, blank=True, null=True)
    special_note=models.TextField()
    is_approve = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    is_finalised = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    status=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name='requisition_by')

    def __str__(self):
        return str(self.created_at)



class RequisitionDetail(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE,related_name='requisition_detail')
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.DecimalField(max_digits=10,decimal_places=2)
    uom=models.ForeignKey(UOM,on_delete=models.SET_NULL,blank=True,null=True)
    status = models.BooleanField(default=True)


    def __str__(self):
        return str(self.requisition.created_at)


    def material_rate(self):
        rate=CompanyProjectDetail.objects.values_list('rate',flat=True).filter(material=self.material)
        value=rate.values('rate')
        return value









