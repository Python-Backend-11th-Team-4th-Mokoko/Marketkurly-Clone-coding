from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta

from shop.models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from shop.forms import ProductFilterForm

### 홈 페이지
def home_page(request):
    categories = Category.objects.all()

    return render(request, 'shop/home.html', {'categories': categories})


# 상품 리스트
def product_list(request, category_slug=None):
    category = None # 안정성을 위해 None 할당
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()

    #카테고리별로 확인
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug) # slug값을 받아 카테고리 선별
        products = products.filter(category=category) # 선별한 카테고리의 상품

    ### 조건별로 상품을 필터링
    if request.method == 'POST':
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            # 배송방식 필터링
            delivery = form.cleaned_data.get('delivery')
            if delivery:
                products = products.filter(delivery=delivery)

            # 포장방식 필터링
            packaging = form.cleaned_data.get('packaging')
            if packaging:
                products = products.filter(packaging=packaging)

            # 가격 필터링
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            if min_price is not None:
                products = products.filter(price__gte=min_price)
            if max_price is not None:
                products = products.filter(price__lte=max_price)

            # 가격 순서 정렬
            array = form.cleaned_data.get('array')
            if array == '낮은가격':
                products = products.order_by('price')  # 가격 오름차순
            elif array == '높은가격':
                products = products.order_by('-price')  # 가격 내림차순
            
            form.clean()
    else:
        form = ProductFilterForm()

    # 카테고리, 모든 카테고리, 상품 정보를 보내 렌더링
    return render(request, 'shop/product/list.html',
                  {'category': category, 'categories': categories, 
                   'products': products, 'cart_product_form': cart_product_form, 'form': form})


### 신상품
def new_products(request):
    categories = Category.objects.all() ### 이게 있어야 이쪽 페이지에서도 카테고리 목록이 열림

    one_week_ago = timezone.now() - timedelta(days=7) # 1주일 이내의 상품만
    new_products = Product.objects.filter(available=True, created__gte=one_week_ago).order_by('-created') #최신상품 순으로 정렬

    ### 조건별로 상품을 필터링
    if request.method == 'POST':
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            # 배송방식 필터링
            delivery = form.cleaned_data.get('delivery')
            if delivery:
                new_products = new_products.filter(delivery=delivery)

            # 포장방식 필터링
            packaging = form.cleaned_data.get('packaging')
            if packaging:
                new_products = new_products.filter(packaging=packaging)

            # 가격 필터링
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            if min_price is not None:
                new_products = new_products.filter(price__gte=min_price)
            if max_price is not None:
                new_products = new_products.filter(price__lte=max_price)

            # 가격 순서 정렬
            array = form.cleaned_data.get('array')
            if array == '낮은가격':
                new_products = new_products.order_by('price')  # 가격 오름차순
            elif array == '높은가격':
                new_products = new_products.order_by('-price')  # 가격 내림차순
            
            form.clean()
    else:
        form = ProductFilterForm()

    return render(request, 'shop/product/new_products.html', 
                  {'categories': categories, 'new_products': new_products, 'form': form})



# 상품 정보
def product_detail(request, id, slug):
    categories = Category.objects.all() ### 이게 있어야 이쪽 페이지에서도 카테고리 목록이 열림
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    total_price = product.price
    updated_quantity = None

    ### 상품 상세 화면에서 변동하는 가격을 즉시 표시해주기 위한 기능, 장바구니로 담는 기능
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            if request.POST.get('action') == '+':
                form.add_quantity(request)
            elif request.POST.get('action') == '-':
                form.subtract_quantity(request)

            quantity = form.cleaned_data['quantity']  # 입력된 수량
            total_price = product.price * quantity  # 총 가격 계산

            # 수량 변경 후 폼의 값을 업데이트
            updated_quantity = form.cleaned_data['quantity']
            form = CartAddProductForm(initial={'quantity': updated_quantity})

            if request.POST.get('action') == 'add_to_cart':
                cart = Cart(request)  # Cart 객체 생성 (세션 기반)
                product_id = request.POST.get('product_id')  # 폼에서 넘어온 상품 ID 가져오기
                cart.add(product=product, quantity=updated_quantity)  # 장바구니에 상품 추가
                cart.save()  # 세션 저장
                
    else:
        form = CartAddProductForm()
    ###

    # 상품정보를 보내 렌더링
    return render(request, 'shop/product/detail.html',
                  {'product': product, 'cart_product_form': form, 
                   'total_price': total_price, 'updated_quantity': updated_quantity, 
                   'categories': categories})
