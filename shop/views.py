from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Bill, BillItem
from .forms import ProductForm, BillItemForm
from django.db import transaction

# shop/views.py
def product_list(request):
    # Logic to retrieve products (if any) and pass to the template
    return render(request, 'shop/products/list.html')  # Adjust the template path as needed


# Add a new product to stock
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add.html', {'form': form})

# Create a new bill and deduct stock
@transaction.atomic
def create_bill(request):
    if request.method == 'POST':
        bill = Bill.objects.create(total_amount=0)  # Placeholder amount
        total_amount = 0
        for item_data in request.POST.getlist('items'):
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = int(item_data['quantity'])
            if product.quantity < quantity:
                # Error handling if stock is insufficient
                continue
            total_price = product.price * quantity
            BillItem.objects.create(bill=bill, product=product, quantity=quantity, total_price=total_price)
            product.quantity -= quantity  # Deduct stock
            product.save()
            total_amount += total_price
        bill.total_amount = total_amount
        bill.save()
        return redirect('bill_detail', bill_id=bill.id)
    return render(request, 'shop/bills/create.html')