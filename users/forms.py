from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('userID', 'email', 'name', 'phone_number', 'address', 'is_owner')  # 회원가입에 필요한 필드들

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['userID'].required = True
        self.fields['email'].required = True
        self.fields['name'].required = True
        self.fields['phone_number'].required = True

class CustomUserChangeForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number', 'address', 'is_owner')  # 수정할 수 있는 필드들

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True
        self.fields['phone_number'].required = True

        # make_date 필드를 읽기 전용으로 추가
        if 'instance' in kwargs:
            self.fields['make_date'] = forms.DateTimeField(initial=kwargs['instance'].make_date, disabled=True)
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('비밀번호가 올바르지 않습니다.')
        return password

class FindUsernameForm(forms.Form):
    email = forms.EmailField(label="이메일", max_length=255)


class CheckPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="비밀번호", required=True)
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')