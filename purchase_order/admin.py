from django.contrib import admin
from .models import PurchaseOrder

class PurchaseOrderAdmin(admin.ModelAdmin):
    model = PurchaseOrder
    
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
