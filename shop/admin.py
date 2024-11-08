# shop/admin.py
from django.contrib import admin
from .models import Product, Bill  # Import your models here

# Register your models here
admin.site.register(Product)
admin.site.register(Bill)
