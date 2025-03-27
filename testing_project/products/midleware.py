from django.conf import settings
from django.http import HttpResponse

"""
* midleware
- django의 요청/응답 처리를 위한 hook 프레임워크
- django의 입력이나 출력을 전역적으로 변경할 수 있는 low level의 plug-in 시스템이라고 한다

이 예제에선 db 업데이트나 마이그레이션같은 작업을 할 때를 유지 관리 모드라고 하여
서비스를 오프라인으로 전환해야 함
"""

class MaintenanceModeMiddleware:
    """
    현재 사이트가 maintenance mode(유지 관리 모드)인 것을 확인하는 미들웨어
    MAINTENANCE_MODE가 Ture이면, "Site under maintenance" 응답을 반환한다.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'MAINTENANCE_MODE', False): # settings에서 MAINTENANCE_MODE를 가져오고(없으면 False) 값이 True면 503응답
            return HttpResponse("Site is under maintenance", status=503)
        return self.get_response(request)