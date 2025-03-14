from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from products.models import Product

"""
database constraints?
- Product의 price, stock_count는 IntegerField다.
- 자체 매서드 clean으로 음수가 안되게 유효성검사를 하지만 데이터베이스에 음수가 저장되기는 한다.
- 그래서 데이터베이스 제약조건이 필요하다!

그러면 clean 매서드는 왜 만든건지?
- form 제출된 시점에 db에 해당 데이터를 보내기 전에 유효성 검사 오류가 있는 경우
- 해당 양식을 반환하고 사용자가 오류를 수정할 수 있게 하여 불필요한 데이터베이스 왕복을 방지하기 위해.
"""

"""
https://docs.djangoproject.com/ko/5.1/topics/testing/tools/#django.test.TestCase.setUpTestData
setUpTestData
- 전체 테스트사례에 대해 *한 번만* 생성됨
- setup의 일부로 데이터베이스에 많은 개체를 만들고, 한 번만 수행하면 되는 경우에 사용
- 당연히 setup보다 빠르다!
"""

class ProductModelTest(TestCase):
    @classmethod #클래스메서드 데코레이터, 매개변수에 self대신 cls로 해야함
    def setUpTestData(cls):
        cls.product = Product(name='Test Product', price=100.00, stock_count=10) # 클래스변수: 모든 인스턴스가 공유함, 접근할땐 똑같이 self.product로

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

            self.product.stock_count = -1
            with self.assertRaises(ValidationError): #매개변수인 예상하는 예외가 발생하지 않으면 테스트 실패, 예상된 예외가 아닌 다른 예외 발생 시에도 실패
                self.product.clean()
    
    def test_negative_price_constraint(self):
        """데이터베이스 제약조건으로 product의 price속성에 음수가 저장이 안되는지 테스트"""
        product = Product(name='negative price product', price=-1.00, stock_count=10)

        with self.assertRaises(IntegrityError):
            product.save()
    
    def test_negative_stock_count_constraint(self):
        """데이터베이스 제약조건으로 product의 stock_count속성에 음수가 저장이 안되는지 테스트"""
        product = Product(name='negative price product', price=1.00, stock_count=-10)
        
        with self.assertRaises(IntegrityError):
            product.save()