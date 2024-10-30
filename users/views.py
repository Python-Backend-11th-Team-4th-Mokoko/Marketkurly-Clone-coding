from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login as app_login
from django.contrib.auth import logout as app_logout
from .forms import CustomUserCreationForm, CustomUserChangeForm, FindUsernameForm, CheckPasswordForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from shop.models import Product
from .models import Wishlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# 이메일 인증을 위한 import
from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from .tokens import account_activation_token
# 장바구니 기능을 위한 import
from cart.cart import Cart
from cart.forms import CartAddProductForm

# Create your views here.
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            app_login(request, form.get_user())

            # 로그인 시 최초 한 번만 DB에서 장바구니 정보를 세션에 병합
            cart = Cart(request)
            if not request.session.get('cart_merged', False):  # 병합 여부 확인
                cart.merge_with_db()  # 병합
                request.session['cart_merged'] = True  # 병합 처리 완료 플래그 설정

            return redirect('shop:home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout(request):
    cart = Cart(request)
    cart.save_to_db()
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
    if request.method == 'POST':
        form = CheckPasswordForm(request.POST, user=request.user)
        
        if form.is_valid():
            # POST 요청이 들어오면 사용자를 삭제하고 로그아웃 처리
            request.user.delete()
            app_logout(request)
            messages.success(request, '회원 탈퇴가 완료되었습니다.')
            return redirect('shop:home')
    else:
        form = CheckPasswordForm(user=request.user)
    # GET 요청 시에는 탈퇴 확인 페이지를 렌더링
    return render(request, 'users/del_user_confirm.html', {'password_form': form})

@login_required
def update_user(request):
    user = request.user
    # 세션에 저장된 password_confirmed 값 가져오기 (기본값은 False)
    password_confirmed = request.session.get('password_confirmed', False)
    password_form = CheckPasswordForm(user=user)
    customuser_form = CustomUserChangeForm(instance=user)
    
    if request.method == 'POST':
        if 'confirm_password' in request.POST:  # 비밀번호 인증 폼 제출 시
            password_form = CheckPasswordForm(request.POST, user=user)
            if password_form.is_valid():
                # 세션에 비밀번호 인증 성공 상태 저장
                request.session['password_confirmed'] = True
                password_confirmed = True
        elif 'update_user' in request.POST and password_confirmed:  # 프로필 수정 폼 제출 시
            customuser_form = CustomUserChangeForm(request.POST, instance=user)
            if customuser_form.is_valid():
                customuser_form.save()  # 변경된 사용자 정보를 저장
                messages.success(request, '프로필이 성공적으로 업데이트되었습니다.')
                # 세션에서 비밀번호 인증 상태 제거
                request.session.pop('password_confirmed', None)
                return redirect('shop:home')
            else:
                messages.error(request, '입력한 정보가 유효하지 않습니다. 다시 확인해 주세요.')
    
    # GET 요청이거나 폼 검증 실패 시 화면 표시
    return render(request, 'users/update.html', {
        'password_form': password_form,
        'customuser_form': customuser_form,
        'password_confirmed': password_confirmed,
    })

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

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'users/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if created:
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            return HttpResponse('이미 찜한 상품입니다.')


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        Wishlist.objects.filter(user=request.user, product=product).delete()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    

@login_required
def wishlist_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)  # 수량을 받기 위한 폼
        if form.is_valid():
            # 폼에서 수량을 가져와 장바구니에 추가
            quantity = form.cleaned_data['quantity']
            cart = Cart(request)  # 세션 기반 Cart 객체 가져오기
            cart.add(product=product, quantity=quantity)  # 장바구니에 추가
            cart.save()  # 세션 저장

        return redirect('users:wishlist')
    else:
        form = CartAddProductForm(initial={'quantity': 1})  # 기본 수량 1로 초기화된 폼 반환
    return redirect('users:wishlist')

