from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Category, Product

from cart.forms import CartAddProductForm
from cart.cart import Cart

### 홈 페이지
def home_page(request):
    context = None
    return render(request, 'shop/home.html', context)


# 상품 리스트
def product_list(request, category_slug=None):
    category = None # 안정성을 위해 None 할당
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug) # slug값을 받아 카테고리 선별
        products = products.filter(category=category) # 선별한 카테고리의 상품

    # 카테고리, 모든 카테고리, 상품 정보를 보내 렌더링
    return render(request, 'shop/product/list.html',
                  {'category': category, 'categories': categories, 'products': products, 'cart_product_form': cart_product_form})


# 상품 정보
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    total_price = product.price
    updated_quantity = None

    ### 상품 상세 화면에서 변동하는 가격을 즉시 표시해주기 위한 기능, 장바구니로 담는 기능
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            if request.POST.get('action') == 'add':
                form.add_quantity(request)
            elif request.POST.get('action') == 'subtract':
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
                  {'product': product, 'cart_product_form': form, 'total_price': total_price, 'updated_quantity': updated_quantity})


    # ### 수량 조절
    # if request.method == 'POST':
    #     if cart_product_form.is_valid():
    #         if request.POST.get('action') == 'add':
    #             cart_product_form.add_quantity(request)
    #         elif request.POST.get('action') == 'subtract':
    #             cart_product_form.subtract_quantity(request)

    # product_quantity = cart_product_form.cleaned_data['quantity']