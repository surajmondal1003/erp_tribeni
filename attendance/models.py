from django.db import models
from authentication.models import EmployeeProfile

# Create your models here.


class Attendance(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.SET_NULL, blank=True, null=True)
    in_time=models.TimeField()
    out_time=models.TimeField()
    date=models.DateTimeField()
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.employee)+''+str(self.date)
