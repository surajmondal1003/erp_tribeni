from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class AppApprove(models.Model):
    content = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    approval_level=models.IntegerField()

    def __str__(self):
        return str(self.content.model)+' level : '+str(self.approval_level)

    def content_id(self):
        return self.content.id


class EmpApprove(models.Model):
    content = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.content)

    def content_details(self):
        id = self.content.id
        name = self.content.model
        details = {'id': id, 'name': name}
        return details


class EmpApproveDetail(models.Model):

    emp_approve=models.ForeignKey(EmpApprove, on_delete=models.SET_NULL, blank=True, null=True,related_name='emp_approve_details')
    emp_level = models.IntegerField()
    primary_emp = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='primary_emp')
    secondary_emp = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name='secondary_emp')

    def primary_emp_details(self):
        id=self.primary_emp.id
        name=self.primary_emp.first_name
        details={'id':id,'name':name}
        return details

    def secondary_emp_details(self):
        id=self.secondary_emp.id
        name=self.secondary_emp.first_name
        details={'id':id,'name':name}
        return details


