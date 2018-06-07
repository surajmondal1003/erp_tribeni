from django.contrib import admin
from purchase_order.models import PurchaseOrder,PurchaseOrderDetail,PurchaseOrderFreight,PurchaseOrderMap,PurchaseOrderTerms

# Register your models here.
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderDetail)
admin.site.register(PurchaseOrderFreight)
admin.site.register(PurchaseOrderTerms)
admin.site.register(PurchaseOrderMap)
