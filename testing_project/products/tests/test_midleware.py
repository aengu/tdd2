from django.test import TestCase, override_settings
from django.urls import reverse
from products.midleware import MaintenanceModeMiddleware

"""
* coverage
https://coverage.readthedocs.io/en/7.7.1/
- 테스트 진행 시 코드의 커버리지를 리포트 해주는 서드파티 라이브러리
- 진행한 테스트 코드들의 run, missing, excluded 여부를 알려준다.

명령어
0. pip install coverage
1. coverage run manage.py test --settings=test_settings
2. coverage report / coverage html

나의 경우 이 파일의 22, 24줄 코드가 missing이 떠서 디버깅 해보니 정말 실행이 안되고 있었다.
알고보니 두 메서드 이름이 같아서 (off/on) 아래 메서드만 실행되었던 것... 복붙 실수
처음에 이걸 해서 효과가 있나 했는데 정말 효과가 있다..
"""

class MainTenanceModeTests(TestCase):

    @override_settings(MAINTENANCE_MODE=False) # 테스트에서 seetings의 설정 값들을 동적으로 변경할 수 있다.
    def test_maintenance_mode_off(self):
        """MAINTENANCE_MODE가 False일 경우, 사이트가 일반적으로 작동하는 것을 테스트"""
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'welcome to our store')
    
    @override_settings(MAINTENANCE_MODE=True)
    def test_maintenance_mode_on(self):
        """MAINTENANCE_MODE가 True일 경우, 사이트가 503 응답을 반환하는 것을 테스트"""
        response = self.client.get(reverse('homepage'))

        self.assertContains(response, 'Site is under maintenance', status_code = 503)