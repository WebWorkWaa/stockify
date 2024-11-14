# shop/admin.py
from django.contrib import admin
from .models import Product, Bill, BillItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity']

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'total_amount']
    readonly_fields = ['total_amount']

@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ['bill', 'product', 'quantity', 'total_price']
