from django.contrib import admin
from purchase_requisition.models import Requisition,RequisitionDetail
# Register your models here.

admin.site.register(Requisition)
admin.site.register(RequisitionDetail)

