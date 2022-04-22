from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.home, name='home_'),
    path('contact/', views.contact, name='contact'),
    path('test/', views.test, name='test'),
]
