from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product

# 홈 페이지
def home_page(request):
    context = None
    return render(request, 'shop/home.html', context)


# 상품 리스트
def product_list(request, category_slug=None):
    category = None # 안정성을 위해 None 할당
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug) # slug값을 받아 카테고리 선별
        products = products.filter(category=category) # 선별한 카테고리의 상품

    # 카테고리, 모든 카테고리, 상품 정보를 보내 렌더링
    return render(request, 'shop/product/list.html',
                  {'category': category, 'categories': categories, 'products': products})


# 상품 정보
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    # 상품정보를 보내 렌더링
    return render(request, 'shop/product/detail.html',
                  {'product': product})
