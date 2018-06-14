from django.db import models
from django.contrib.auth.models import User
from company.models import Company
from departments.models import Departments
from designation.models import Designation
from states.models import State

# Create your models here.

class EmployeeProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name='employee_profile_details')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    departments = models.ForeignKey(Departments, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact=models.CharField(max_length=255)
    dob=models.DateTimeField()
    alt_contact=models.CharField(max_length=255)
    pan = models.CharField(max_length=100,blank=True,null=True)
    blood_group =models.CharField(max_length=100,blank=True,null=True)
    adhaar_no=models.CharField(max_length=100,blank=True,null=True)
    epf_status=models.BooleanField(default=False)
    epf_no=models.CharField(max_length=100)
    emp_present_address=models.CharField(max_length=255)
    emp_present_state=models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True,related_name='emp_present_state')
    emp_present_city=models.CharField(max_length=100)
    emp_present_pin=models.CharField(max_length=100)
    emp_permanent_address = models.CharField(max_length=255,blank=True,null=True)
    emp_permanent_state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True,related_name='emp_permanent_state')
    emp_permanent_city = models.CharField(max_length=100,blank=True,null=True)
    emp_permanent_pin = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name='emp_created_by')
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


    def company_details(self):
        id = self.company.id
        name = self.company.company_name
        details = {'id': id, 'name': name}
        return details

    def department_details(self):
        id = self.departments.id
        name = self.departments.department_name
        details = {'id': id, 'name': name}
        return details

    def designation_details(self):
        id = self.designation.id
        name = self.designation.designation_name
        details = {'id': id, 'name': name}
        return details

    def created_by_details(self):
        id = self.created_by.id
        name = self.created_by.username
        details = {'id': id, 'name': name}
        return details

    def __str__(self):
        return str(self.first_name)
