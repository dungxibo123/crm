from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("HAHA")
def contact(r):
    return HttpResponse("Hehe")
def test(r):
    return HttpResponse("Hihi")
