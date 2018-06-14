from django.db import models
from states.models import State
from django.contrib.auth.models import User
from company.models import Company


# Create your models here.

class Transport(models.Model):
    company=models.ForeignKey(Company,on_delete=models.SET_NULL,blank=True,null=True)
    transporter_name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.BigIntegerField()
    state=models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True)
    city=models.CharField(max_length=150)
    pin=models.CharField(max_length=100)
    pan=models.CharField(max_length=255)
    gstin=models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.transporter_name)
