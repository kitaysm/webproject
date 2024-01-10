
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    # 추가적인 필드나 로직을 원하는 대로 작성할 수 있습니다.
    pass


# \single_pages\forms.py

from django.contrib.auth.forms import AuthenticationForm

class CustomLogoutForm(AuthenticationForm):
    pass

