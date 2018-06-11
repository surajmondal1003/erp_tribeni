from django.contrib import admin
from stock.models import Stock,StockIssue,StockTransfer,StockView

# Register your models here.
admin.site.register(Stock)
admin.site.register(StockIssue)
admin.site.register(StockTransfer)
admin.site.register(StockView)