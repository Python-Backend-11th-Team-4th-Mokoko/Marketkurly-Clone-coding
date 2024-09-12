from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('product_create/', views.product_create, name='product_create'),
    path('product_seller/<str:username>/', views.product_seller, name='product_seller'),
    path('product_delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('product_update/<int:pk>/', views.product_update, name='product_update'),
    path('sold_history/', views.sold_history, name='sold_history'),
    path('order_history/', views.order_history, name='order_history'),
]
