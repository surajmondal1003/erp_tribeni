from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UOM(models.Model):
    name=models.CharField(max_length=25)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return str(self.name)