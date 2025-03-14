from django.contrib import admin
from django.urls import path
from products.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage)
]
