from testing_project.settings import *
"""
MAINTENANCE_MODE가 True인 상태로 전체 테스트를 돌려버리면 (python manage.py test)
testing_forms부터 실행하기 때문에 당연히 실패한다
그럴 때는
방법1. 별도의 테스트 전용 설정모듈 만들기
    python manage.py test --settings=test_settings
    이렇게 test_settings라는 설정모듈을 지정하여 테스트하면 된다.

방법2. 테스트클래스에 override_settings 데코레이터 달기.
    @override_settings(MAINTENANCE_MODE=True)
    class ProductFormTest(TestCase):
"""
MAINTENANCE_MODE = False