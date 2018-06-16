from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class AppApprove(models.Model):
    content = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    approval_level=models.IntegerField()

    def __str__(self):
        return str(self.content.name)+' level : '+str(self.approval_level)


class EmpApprove(models.Model):
    content = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True)
    emp_level=models.IntegerField()
    primary_emp=models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name='primary_emp')
    secondary_emp=models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name='secondary_emp')


