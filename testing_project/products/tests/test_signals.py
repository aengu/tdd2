from django.test import TestCase
from unittest.mock import patch
from products.models import User

class UserSignalsTest(TestCase):

    @patch('products.signals.send_mail')
    def test_welcome_email_sent_on_user_creation(self, mock_send_mail):
        # signal에 triger되도록 새 유저 생성
        User.objects.create_user(username='test_user', password='password123', email='test@example.com')

        mock_send_mail.assert_called_once_with(
            'Welcome!', # 제목
            'Thanks for signing up!', # 본문
            'admin@django.com',  # 송신 이메일
            ['test@example.com'],    # 수신 이메일 리스트
            fail_silently=False,
        )
    
    @patch('products.signals.send_mail')
    def test_no_email_sent_on_user_creation(self, mock_send_mail):
        user = User.objects.create_user(username='test_user', password='password123', email='test@example.com')

        # mock의 호출 횟수를 0으로 초기화
        mock_send_mail.reset_mock()

        # user 업데이트 (이번엔 signal이 이메일 전송하지 않아야 한다)
        user.email = 'updated_email@example.com'
        user.save()

        # 이메일 전송 메서드가 호출되지 않음을 확인
        mock_send_mail.assert_not_called()