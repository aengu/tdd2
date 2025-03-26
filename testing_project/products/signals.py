from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

"""
shell에서 create_user할 때 email을 넣어야 한다;
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