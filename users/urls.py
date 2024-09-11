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
]