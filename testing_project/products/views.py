from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
import requests
from requests.exceptions import RequestException
from django.http import JsonResponse, HttpResponse

"""
테스트 중에 request.get 호출을 모의(mock)해야 하는 이유?
1. 테스트 속도 개선
    - 네트워크 요청은 상대적으로 느리며 응답시간이 일정하지 않음.
2. 외부 서비스 의존성 제거
    - 외부 서비스(여기선 jsonplaceholder)의 상태에 따라 테스트가 실패할 수도 있음
"""

def post(request):
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        response.raise_for_status() # http 요청이 실패할 시(4xx, 5xx) HTTPError 발생
        return JsonResponse(response.json())
    except RequestException as e:
        # log in a real application

        # return a 503 service unavailable response
        return HttpResponse('Service Unavailable', status=503)


@login_required
def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')


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

