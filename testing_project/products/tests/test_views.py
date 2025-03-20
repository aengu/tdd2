from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from products.models import Product, User

"""
전체 테스트 진행 명령어
python manage.py test

이 파일만 테스트하고 싶다면
python manage.py test products.tests.test_views
"""

"""
TestCase, SimpleTestCase 차이점
- 기존 TestCase는 각 테스트마다 새로운 데이터베이스 트랜잭션을 생성/롤백하기 때문에 성능 비용이 큼
- 그래서 데이터베이스 쿼리가 필요없는 테스트(유틸리티 함수, 템플릿 테스트 등)에는 SimpleTestCase를 사용하는게 좋다.
- 실제로 SimpleTestCase에서 query사용하면 DatabaseOperationForbidden 오류가 뜨면서 TestCase나 TransactionTestCase를 사용하라고 나온다.
"""

"""
assertContains
- 응답이 일부 콘텐츠를 성공적으로 가져왔음을 나타내는지(HTTP 상태 코드가 예상된 값인지) 그리고 특정 텍스트가 응답 본문에서 count번 나타나는지를 확인
- 만약 count가 None이면, 해당 텍스트가 적어도 한 번 이상 포함되어 있으면 검증 성공
- 텍스트만 되지, Product 특정 객체가 있는지(self.assertContains(response, p)) 이런식은 안되나보다.
"""

"""
1. User.objects.create(**user_data)
2. User.objects.create_user(**user_data)
1번처럼 유저객체 만들면 안된다.. 저러면 그냥 password에 'password123'라는 plain text가 저장됨.
2번처럼 creatr_user로 만들어야 password에 해싱된 값으로 저장됨.
해싱된 암호를 비교하여 로그인하는거라 1번처럼 만들면 인증 다 안된다... 아니 이걸 까먹다니
"""

class TestProfilePage(TestCase):

    def test_profile_view_accesible_for_anonymose_users(self):
        "로그인 하지 않은 유저가 profile페이지에 접근할 경우 login페이지로 리디렉션되는지 테스트"
        response = self.client.get(reverse('profile'))

        # 리디렉트되는지 확인
        self.assertRedirects(response, expected_url=f"{reverse('login')}?next={reverse('profile')}")

    def test_profile_view_accessible_for_authenticated_users(self):
        "로그인한 유저가 profile페이지에 접근하여 username이 제대로 나오는지 테스트"
        # 테스트 유저 생성
        user_data = {
            'username' : 'test_user',
            'password' : 'password123'
        }
        User.objects.create_user(**user_data)

        # 테스트유저 로그인
        # response = self.client.post(reverse('login'), data=data) # 아래가 더 직관적
        self.client.login(username='test_user', password='password123')
        response = self.client.get(reverse('profile'))

        # response content에 username이 포함되어 있는지 확인
        self.assertContains(response, 'test_user')


class TestHomePage(SimpleTestCase):

    # def test_db_query(self):
    #     product = Product(name='negative price product', price=1.00, stock_count=-10)
    #     product.save()
    """
    FAIL: test_db_query (products.tests.test_views.TestHomePage)
    raise DatabaseOperationForbidden(self.message)
    django.test.testcases.DatabaseOperationForbidden: Database queries to 'default' are not allowed in SimpleTestCase subclasses. Either subclass TestCase or TransactionTestCase to ensure proper test isolation or add 'default' to products.tests.test_views.TestHomePage.databases to silence this failure.
    """

    # def test_homepage_status_code(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)
    
    def test_homepage_use_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    
    def test_homepage_contain_welcome_msg(self):
        """
        assertContains
        - 매개변수 status_code의 기본값이 200이므로 이 테스트를 한다면 기본적으로
        status_code가 200인지 확인하는 테스트는 필요없다.
        """
        response = self.client.get('/')
        self.assertContains(response, 'welcome to our store')

class TestProductPage(TestCase):
    def setUp(self):
        Product.objects.create(name="Laptop", price=1000, stock_count=3)
        Product.objects.create(name="Phone", price=800, stock_count=5)
    
    def test_products_uses_correct_template(self):
        response = self.client.get(reverse('products'))
        self.assertTemplateUsed(response, 'products.html')
    
    def test_products_context(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(len(response.context['products']), 2)
        self.assertContains(response, "Laptop")
        self.assertContains(response, "Phone")
        self.assertNotContains(response, "no products available")
    
    def test_products_no_context(self):
        """products가 없는 경우, 안내 메세지가 나오는지 테스트"""
        Product.objects.all().delete()
        response = self.client.get(reverse('products'))
        self.assertContains(response, "no products available")
        # self.assertEqual(len(response.context), 0) # 이제 context에 form도 포함되므로 context['products']로 접근해야함
        self.assertQuerysetEqual(response.context['products'], [])