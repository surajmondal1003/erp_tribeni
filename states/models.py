from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class State(models.Model):
    state_name=models.CharField(max_length=50)
    tin_number=models.IntegerField()
    state_code=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    status=models.BooleanField(default=True)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.state_name)