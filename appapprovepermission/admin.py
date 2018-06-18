from django.contrib import admin
from appapprovepermission.models import AppApprove,EmpApprove,EmpApproveDetail
# Register your models here.
admin.site.register(AppApprove)
admin.site.register(EmpApprove)
admin.site.register(EmpApproveDetail)