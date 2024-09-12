from django.shortcuts import render,redirect
from django.contrib.auth import login as app_login
from django.contrib.auth import logout as app_logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# 이메일 인증을 위한 import
from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import FindUsernameForm

# Create your views here.
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            app_login(request, form.get_user())
            return redirect('shop:home')
    else:
        form = AuthenticationForm()
    content = {'form' : form}
    return render(request, 'users/login.html',content)

def logout(request):
    app_logout(request)
    return redirect('shop:home')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            app_login(request, user)
            return redirect('shop:home')
    else:
        form=CustomUserCreationForm()
    content = {'form' : form}
    return render(request, 'users/signup.html', content)

def del_user(request):
    user = request.user
    if request.method == 'POST':
        # POST 요청이 들어오면 사용자를 삭제하고 로그아웃 처리
        user.delete()
        app_logout(request)
        return redirect('shop:home')
    
    # GET 요청 시에는 탈퇴 확인 페이지를 렌더링
    return render(request, 'users/del_user_confirm.html')

def update_user(request):
    # 현재 로그인한 사용자 인스턴스를 가져옴
    user = request.user

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)  # 인스턴스를 전달
        if form.is_valid():
            user_instance = form.save(commit=False)  # 사용자 인스턴스를 일단 저장하지 않고 반환
            user_instance.make_date = user.make_date  # make_date 필드를 기존 값으로 유지
            user_instance.save()  # 실제 저장
            return redirect('shop:home')
    else:
        # GET 요청에서는 기존 사용자 데이터를 폼에 미리 채워서 보냄
        form = CustomUserChangeForm(instance=user)

    content = {'form': form}
    return render(request, 'users/update.html', content)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('shop:home')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form' : form}
    return render(request, 'users/change_password.html', context)

def send_username_email(request):
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                userID = User.objects.get(email=email)
                # 인증 링크 생성
                domain = request.get_host()
                uid = urlsafe_base64_encode(force_bytes(userID.pk))
                token = account_activation_token.make_token(userID)
                # 이메일 내용 생성
                mail_subject = '아이디 찾기 인증 메일'
                message = render_to_string('users/find_username_email.html', {
                    'userID': userID,
                    'domain' : domain,
                    'uid': uid,
                    'token': token,
                })
                send_mail(mail_subject, message, 'cw9094@naver.com', [email])
                return HttpResponse('인증 메일이 발송되었습니다. 이메일을 확인해주세요.')
            except User.DoesNotExist:
                return HttpResponse('해당 이메일로 등록된 사용자가 없습니다.')
    else:
        form = FindUsernameForm()

    return render(request, 'users/find_username.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        return HttpResponse(f'아이디는 {user.userID}입니다.')
    else:
        return HttpResponse('링크가 유효하지 않거나 만료되었습니다.')


def my_page(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('users:login') 

    context = {
        'user': user,
        'links': {
            'update_user': 'users:update_user',  
            'change_password': 'users:change_password', 
            'order_history': 'shop:order_history',
        }
    }
    return render(request, 'users/my_page.html', context)

