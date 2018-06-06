from django.db import models
from states.models import State
from company.models import Company
from django.contrib.auth.models import User

# Create your models here.

class CompanyProject(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='company_project')
    project_name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    project_address=models.CharField(max_length=100,blank=True,null=True)
    project_state=models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True)
    project_city=models.CharField(max_length=100,blank=True,null=True)
    project_pincode=models.CharField(max_length=50,blank=True,null=True)
    project_contact_no=models.BigIntegerField(blank=True,null=True)
    contact_person = models.CharField(max_length=50,blank=True,null=True)
    project_gstin=models.CharField(max_length=50,blank=True,null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.project_name)



class ProjectDetail(models.Model):
    project=models.ForeignKey(CompanyProject,on_delete=models.CASCADE,related_name='project_details')







