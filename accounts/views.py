from django.shortcuts import render,redirect
from .models import *
from .filter import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponse
from .forms import OrderForm, CustomerForm
from .decorators import *
# Create your views here.



@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin', 'Customer'])
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


def logout_user(r):
    logout(r)
    return redirect('/login')


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
@allowed_users(allowed_roles=['admin','Customer'])
def create_order(r,pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(r.POST or None, initial={'customer': customer})
    if form.is_valid():
        form.save()
    context = {'form': form, 'customer': customer}
    return render(r, 'accounts/order_form.html', context)
@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def update_order(r, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(r.POST or None, instance=order)
    if form.is_valid():
        form.save()
    context = {'form': form, 'order': order}
    return render(r, 'accounts/order_form.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def delete_order(r, pk):
    order = Order.objects.get(id=pk)
    if r.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(r, 'accounts/delete.html', context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def create_customer(r):
    form = CustomerForm(r.POST or None)
    if form.is_valid():
        form.save()
    context = {'form': form}
    return render(r, 'accounts/customer_form.html', context)
@unauthenticated_user
def register_page(r):
    form = UserCreationForm()
    if r.method == 'POST':
        form = UserCreationForm(data=r.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            #    name=user.username,
            )
            messages.success(r, 'Account created successfully for' + username)
            return redirect('/login')
    context = {}
    return render(r, 'accounts/register.html')
@unauthenticated_user
def login_page(r):
    if r.method == 'POST':
        username = r.POST.get('username')
        password = r.POST.get('password')
        user = authenticate(r, username=username, password=password)
        if user is not None:
            login(r, user)
            return redirect('/user')
        else:
            messages.info(r, 'Username or Password is incorrect')
    context = {}
    return render(r, 'accounts/login.html')
@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin', 'Customer'])
def user_page(r):
    orders = r.user.customer.order_set.all()
     
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'total_order': total_order, 'delivered': delivered, 'pending': pending}
    return render(r, 'accounts/user.html', context)


@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin', 'Customer'])
def account_settings(r):
    customer = r.user.customer
    form = CustomerForm(r.POST or None, instance=customer)
    if r.method == 'POST':
        form = CustomerForm(r.POST or None, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(r, 'accounts/account_settings.html', context)





