from django.shortcuts import render
from .models import *


from django.http import HttpResponse
# Create your views here.
def home(r):
    orders = Order.objects.all()
    customer = Customer.objects.all()
    total_customer = Customer.objects.all().count()
    total_order = Order.objects.all().count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customer, 'total_customer': total_customer,
               'total_order': total_order, 'delivered': delivered, 'pending': pending}
    return render(r, './accounts/dashboard.html', context )
def products(r):
    products = Product.objects.all()
    return render(r, 'accounts/products.html', {'products': products})
def customer(r, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer': customer, 'orders': orders, 'order_count': order_count}
    return render(r, 'accounts/customer.html', context)

