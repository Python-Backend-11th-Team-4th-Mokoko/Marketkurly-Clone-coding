from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    # 비밀번호 재설정 URL 패턴
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',template_name='users/password_reset.html'), 
        name='password_reset'),
    
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
        name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
        name='password_reset_confirm'),
    
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
        name='password_reset_complete'),
]