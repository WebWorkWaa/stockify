from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Bill, BillItem
from .forms import ProductForm, BillItemForm
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# shop/views.py

# Cashier Login View
def cashier_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cashier_dashboard')  # Replace with the actual dashboard URL name
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('cashier_login')
    return render(request, 'shop/cashier_login.html')

# Cashier Logout View
@login_required
def cashier_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('cashier_login')

# Cashier Dashboard View
@login_required
def cashier_dashboard(request):
    return render(request, 'shop/cashier_dashboard.html')

# Display the product list
@login_required
def product_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'shop/products/list.html', {'products': products})

# Add a new product to stock
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('product_list')
        else:
            messages.error(request, "Error adding product.")
    else:
        form = ProductForm()
    return render(request, 'shop/products/add.html', {'form': form})

# Create a new bill and deduct stock
@transaction.atomic
@login_required
def create_bill(request):
    if request.method == 'POST':
        bill = Bill.objects.create(total_amount=0)  # Placeholder amount
        total_amount = 0
        insufficient_stock = False

        # Loop through the items to add them to the bill
        for item_data in request.POST.getlist('items'):
            product_id = item_data.get('product_id')
            quantity = int(item_data.get('quantity'))
            product = get_object_or_404(Product, id=product_id)

            if product.quantity < quantity:
                messages.error(request, f"Insufficient stock for product: {product.name}")
                insufficient_stock = True
                continue

            total_price = product.price * quantity
            BillItem.objects.create(bill=bill, product=product, quantity=quantity, total_price=total_price)
            product.quantity -= quantity  # Deduct stock
            product.save()
            total_amount += total_price

        if insufficient_stock:
            messages.error(request, "Some items could not be added due to insufficient stock.")

        bill.total_amount = total_amount
        bill.save()

        return redirect('bill_detail', bill_id=bill.id)

    return render(request, 'shop/bills/create.html')

# View bill details
@login_required
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill_items = BillItem.objects.filter(bill=bill)
    return render(request, 'shop/bills/detail.html', {'bill': bill, 'bill_items': bill_items})
