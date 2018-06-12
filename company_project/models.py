from django.db import models
from states.models import State
from company.models import Company
from django.contrib.auth.models import User
from material_master.models import MaterialType,Material
# from purchase_requisition.models import RequisitionDetail

# Create your models here.

class CompanyProject(models.Model):
    STATUS_CHOICES = (
        ('2', 'False'),
        ('1', 'True'),
        ('0', 'None'),
    )
    company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='company_project')
    project_name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    project_address=models.CharField(max_length=100,blank=True,null=True)
    project_state=models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True)
    project_city=models.CharField(max_length=100,blank=True,null=True)
    project_pincode=models.CharField(max_length=50,blank=True,null=True)
    project_contact_no=models.BigIntegerField(blank=True,null=True)
    contact_person = models.CharField(max_length=100,blank=True,null=True)
    project_gstin=models.CharField(max_length=50,blank=True,null=True)
    engineer_name = models.CharField(max_length=100, blank=True, null=True)
    engineer_contact_no = models.BigIntegerField(blank=True, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_approve = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    is_finalised = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')

    def __str__(self):
        return str(self.project_name)

    # def requistion_details(self):
    #     requisition = RequisitionDetail.objects.filter(requisition__project=self)
    #     response_data = {}
    #     for i in requisition:
    #         data = []
    #         data['requisition_no'] = i.requisition.requisition_no
    #         data['material_type'] = i.material_type.material_type
    #         data['material_name'] = i.material.material_fullname
    #         data['quantity'] = i.quantity
    #         data['avail_qty'] = i.avail_qty
    #         data['uom'] = i.uom.name
    #
    #         response_data.update({data})
    #
    #     return response_data


class CompanyProjectDetail(models.Model):
    project=models.ForeignKey(CompanyProject,on_delete=models.CASCADE,related_name='project_details')
    materialtype = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    boq_ref = models.CharField(max_length=50,blank=True,null=True)
    rate=models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    avail_qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.project)












