from django.contrib import admin
from purchase_invoice.models import PurchaseInvoice,PurchaseInvoiceDetail

# Register your models here.
admin.site.register(PurchaseInvoice)
admin.site.register(PurchaseInvoiceDetail)
