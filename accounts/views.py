from django.shortcuts import render


from django.http import HttpResponse
# Create your views here.
def home(r):
    return render(r, './accounts/dashboard.html')
def products(r):
    return render(r, 'accounts/products.html')
def customer(r):
    return HttpResponse("Hihi")

