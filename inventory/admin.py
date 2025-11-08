from django.contrib import admin
from .models import Item, Supplier, StockIn

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("sku","name","unit","stock_on_hand","reorder_level","location")
    search_fields = ("sku","name")

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name","contact","address")
    search_fields = ("name",)

@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display = ("id","item","supplier","quantity","unit_cost","delivered_at","invoice_no","created_by")
    list_filter = ("delivered_at","supplier")
    search_fields = ("invoice_no",)
