from django.db import models
from django.contrib.auth.models import User
from company.models import Company

# Create your models here.


class Bank(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    bank_name=models.CharField(max_length=255)
    bank_branch=models.CharField(max_length=255)
    bank_ifsc=models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.bank_name)



