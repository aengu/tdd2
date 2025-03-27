from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

"""
https://docs.djangoproject.com/ko/5.1/topics/signals/
* signal
- django에서는 signal dispatcher(신호 전달자?)가 있어 프레임워크 안에 분리된 어플레이케이션 사이에 발생하는 동작을 감지할 수 있다.
- 특정 발신자가 여러 이벤트가 발생했음을 다수의 수신자에게 알릴 수 있다.
- signal을 개발자가 임의로 만들 수 있지만 보통 django에서 제공하는 것을 사용한다 post/pre save,init,migrate 등등
- 이 signal을 받으려면 callback함수인 receiver를 등록해야 한다.
"""

"""
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Welcome!
From: admin@django.com
To: aaa@gmail.com
Date: Wed, 26 Mar 2025 08:09:37 -0000
Message-ID: 
 <174297657746.43669.5232015802349718450@sinhyelan-ui-MacBookPro.local>

Thanks for signing up!
"""
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """새로운 유저가 생성될 때, 웰컴메일 전송"""
    if created and instance.email:
        send_mail(
            'Welcome!', # 제목
            'Thanks for signing up!', # 본문
            'admin@django.com',  # 송신 이메일
            [instance.email],    # 수신 이메일 리스트
            fail_silently=False,
        )