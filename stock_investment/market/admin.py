from django.contrib import admin
from .models import AddMoney, Stock, Transaction, PurchasedStock

admin.site.register(AddMoney)
admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(PurchasedStock)

# Register your models here.
