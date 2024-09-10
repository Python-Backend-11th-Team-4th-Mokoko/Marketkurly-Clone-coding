from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"
urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('del_user/', views.del_user, name="del_user"),
    path('update_user/', views.update_user, name="update_user"),
    path('password/', views.change_password, name='change_password'),
    # 아이디 찾기 URL 패턴
    path('find-username/', views.send_username_email, name='find_username'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # 비밀번호 재설정 URL 패턴
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
        name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
        name='password_reset_confirm'),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
        name='password_reset_complete'),
]