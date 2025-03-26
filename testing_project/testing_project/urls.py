from django.contrib import admin
from django.urls import path
from products.views import homepage, products, profile, login, post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('products/', products, name='products'),
    path('profile/', profile, name='profile'),
    path('login/', login, name='login'),
    path('post/', post, name='post'),
]
