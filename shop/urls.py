from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_page, name='home'), # localhost/ 에서 보이는 기본페이지
    path('lists/', views.product_list, name='product_list'),
    path('lists/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('lists/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]

