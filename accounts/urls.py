from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home_'),
    path('products/', views.products),
    path('customer/', views.customer)
]
