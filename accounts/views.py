from django.shortcuts import render,redirect
from .models import *
from .filter import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import OrderForm, CustomerForm
# Create your views here.



@login_required(login_url='/login')
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
    filt = OrderFilter(r.GET, queryset=orders)
    orders = filt.qs

    order_count = orders.count()
    context = {'customer': customer, 'orders': orders, 'order_count': order_count, "filter": filt}
    return render(r, 'accounts/customer.html', context)
@login_required(login_url='/login')
def create_order(r,pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(r.POST or None, initial={'customer': customer})
    if form.is_valid():
        form.save()
    context = {'form': form, 'customer': customer}
    return render(r, 'accounts/order_form.html', context)
@login_required(login_url='/login')
def update_order(r, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(r.POST or None, instance=order)
    if form.is_valid():
        form.save()
    context = {'form': form, 'order': order}
    return render(r, 'accounts/order_form.html', context)


def delete_order(r, pk):
    order = Order.objects.get(id=pk)
    if r.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(r, 'accounts/delete.html', context)


def create_customer(r):
    form = CustomerForm(r.POST or None)
    if form.is_valid():
        form.save()
    context = {'form': form}
    return render(r, 'accounts/customer_form.html', context)

def register_page(r):
    if r.user.is_authenticated:
        return redirect('/')
    else:
        form = UserCreationForm()
        if r.method == 'POST':
            form = UserCreationForm(data=r.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(r, 'Account created successfully for' + user)
                return redirect('/login')
        context = {}
        return render(r, 'accounts/register.html')
def login_page(r):
    if r.method == 'POST':
        username = r.POST.get('username')
        password = r.POST.get('password')
        user = authenticate(r, username=username, password=password)
        if user is not None:
            login(r, user)
            return redirect('/')
        else:
            messages.info(r, 'Username or Password is incorrect')
    context = {}
    return render(r, 'accounts/login.html')
























