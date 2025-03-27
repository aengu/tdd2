from django.test import TestCase, override_settings
from django.urls import reverse
from products.midleware import MaintenanceModeMiddleware

class MainTenanceModeTests(TestCase):

    @override_settings(MAINTENANCE_MODE=False) # 테스트에서 seetings의 설정 값들을 동적으로 변경할 수 있다.
    def test_maintenance_mode_off(self):
        """MAINTENANCE_MODE가 False일 경우, 사이트가 일반적으로 작동하는 것을 테스트"""
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'welcome to our store')
    
    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_mode_off(self):
        """MAINTENANCE_MODE가 True일 경우, 사이트가 503 응답을 반환하는 것을 테스트"""
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'Site is under maintenance', status_code = 503)