from django.contrib import admin
from stock.models import Stock,StockIssue,StockTransfer

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockIssue)
admin.site.register(StockTransfer)