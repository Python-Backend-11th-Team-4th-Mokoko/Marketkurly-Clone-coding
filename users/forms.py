from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
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
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('email', 'name', 'phone_number', 'address', 'is_owner')  # 수정할 수 있는 필드들

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True
        self.fields['phone_number'].required = True

class FindUsernameForm(forms.Form):
    email = forms.EmailField(label="이메일", max_length=255)