from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('my_page/', views.my_page, name='my_page'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('del_user/', views.del_user, name="del_user"),
    path('update_user/', views.update_user, name="update_user"),
    path('password/', views.change_password, name='change_password'),
    # 아이디 찾기 URL 패턴
    path('find-username/', views.send_username_email, name='find_username'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    #찜 기능
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/cart/<int:product_id>/', views.wishlist_to_cart, name='wishlist_to_cart'),
    path('wishlist/', views.wishlist, name='wishlist')
]