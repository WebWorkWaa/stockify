from django.urls import path
from . import views

urlpatterns = [
    path('cashier/login/', views.cashier_login, name='cashier_login'),
    path('cashier/logout/', views.cashier_logout, name='cashier_logout'),
    path('cashier/dashboard/', views.cashier_dashboard, name='cashier_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('bills/create/', views.create_bill, name='create_bill'),
]
