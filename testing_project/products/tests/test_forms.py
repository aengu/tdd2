from django.test import TestCase
from django.urls import reverse
from products.models import Product
from products.forms import ProductForm

class ProductFormTest(TestCase):

    def test_create_product_when_submitting_valid_form(self):
        """유효한 데이터로 폼이 작성될 시, product가 정상적으로 생성되는지 테스트"""
        form_data = {
            'name': 'test3',
            'price': 300.00,
            'stock_count': 2
        }
        response = self.client.post(reverse('products'), data = form_data)
        
        # product가 잘 생성되었는지, 리다이렉트가 잘 되었는지 확인
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(**form_data).exists())
    
    def test_dont_create_product_when_submitting_invalid_form(self):
        """ 유효하지 않은 폼을 작성하여, product가 생성되지 않는 것을 테스트"""
        form_data = {
            'name': '',
            'price': -300.00,
            'stock_count': -2
        }
        response = self.client.post(reverse('products'), data = form_data)
        
        # product가 생성되지 않는지, 리다이렉트되지 않고 오류메세지를 확인
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(**form_data).exists())
        self.assertTrue('form' in response.context) # 검증에 실패하여 context에 form을 포함하는지 확인

        form = response.context['form']
        self.assertFormError(form, 'name', 'This field is required.')
        self.assertFormError(form, 'price', 'Price cannot be negative')
        self.assertFormError(form, 'stock_count', 'stock_count cannot be negative')