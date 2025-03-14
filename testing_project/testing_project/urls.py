from django.contrib import admin
from django.urls import path
from products.views import homepage, products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('products', products, name='products')
]
