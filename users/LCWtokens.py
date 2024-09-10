from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

##아이디를 이메일인증으로 찾기 위한 토큰 코드
'''account_activation_token은 Django의 PasswordResetTokenGenerator 클래스를 기반으로 하며, 
고유한 토큰을 생성하고 이를 검증하는 데 사용됩니다. 이메일로 보내진 인증 링크에서 해당 토큰을 
확인하여, 사용자가 해당 이메일의 소유자인지 확인하는 중요한 역할을 합니다.'''

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # 유저의 고유 정보를 바탕으로 해시값을 생성하여 토큰의 고유성을 보장
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()