from django.db import models
from django.contrib.auth.models import User
from company.models import Company


# Create your models here.
class Departments(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    department_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.department_name)