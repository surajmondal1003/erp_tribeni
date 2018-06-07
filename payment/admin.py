from django.contrib import admin
from payment.models import Payment,PaymentMap

# Register your models here.
admin.site.register(PaymentMap)
admin.site.register(Payment)