from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

# Create your views here.
def homepage(request):
    return render(request, 'index.html')

def products(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
        else:
            context = {'products': products, 'form': form}
    else:
        context = {'products': products, 'form': ProductForm()}

    return render(request, 'products.html', context)

