from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart_update/<int:product_id>', views.cart_update, name='cart_update'),
    path('', views.cart_detail, name='cart_detail'),
]
