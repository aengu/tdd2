from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product(name='Test Product', price=100.00, stock_count=10)

    def test_in_stock_property(self):
        self.assertTrue(self.product.is_stock)

        #stock_count를 0으로 설정하고 다시 테스트
        self.product.stock_count = 0
        self.assertFalse(self.product.is_stock)
    
    def test_get_discount_price(self):
        self.assertEqual(self.product.get_discounted_price(10), 90)
        self.assertEqual(self.product.get_discounted_price(100), 0)
        self.assertEqual(self.product.get_discounted_price(0), 100)
    
    def test_negative_price_validation(self):
        self.product.clean()

        self.product.price = -1
        with self.assertRaises(ValidationError): #매개변수인 예상하는 예외가 발생하지 않으면 테스트 실패, 예상된 예외가 아닌 다른 예외 발생 시에도 실패
            self.product.clean()
    
def test_negative_stock_validation(self):
        self.product.clean()

        self.product.stock = -1
        with self.assertRaises(ValidationError): #매개변수인 예상하는 예외가 발생하지 않으면 테스트 실패, 예상된 예외가 아닌 다른 예외 발생 시에도 실패
            self.product.clean()