from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GSTrates(models.Model):
    gst_pattern=models.CharField(max_length=100)
    igst=models.DecimalField(max_digits=10,decimal_places=2)
    cgst=models.DecimalField(max_digits=10,decimal_places=2)
    sgst=models.DecimalField(max_digits=10,decimal_places=2)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.gst_pattern)