from django.test import TestCase, SimpleTestCase

"""
전체 테스트 진행 명령어
python manage.py test

이 파일만 테스트하고 싶다면
python manage.py test products.tests.test_views
"""

class TestHomePage(SimpleTestCase):

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_use_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')
    
    def test_homepage_contain_welcome_msg(self):
        response = self.client.get('/')
        self.assertContains(response, 'welcome to our store')