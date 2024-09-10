from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from shop.models import Product, Category
from cart.cart import Cart
from cart.forms import CartAddProductForm


# Create your views here.
#품목 추가
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id) #id가 해당 상품인걸 찾아서 product에 넣음
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override']) #위에서 설정한 변수들이 들어감
    
    return redirect('cart:cart_detail')

#품목 삭제
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


### 체크박스 품목 삭제 옵션
def cart_remove_selected(request):
    if request.method == "POST":
        remove_items = request.POST.getlist('remove_items')  # 체크된 항목들 리스트
        cart = Cart(request)

        for product_id in remove_items:
            product = Product.objects.get(id=product_id)
            cart.remove(product)

        return redirect('cart:cart_detail')  # 장바구니 화면으로 리디렉션

### 카트 내 품목 수량 변경
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        if request.POST.get('action') == '+': # 1 더함
            cart.add(product, quantity=1, override_quantity=False)

        elif request.POST.get('action') == '-': # 1 뺌
            if cart.cart[str(product.id)]['quantity'] > 1:
                cart.add(product, quantity=-1, override_quantity=False)
    
    return redirect('cart:cart_detail')


### 카트 표현부분
def cart_detail(request):
    categories = Category.objects.all() ### 이게 있어야 이쪽 페이지에서도 카테고리 목록이 열림
    cart = Cart(request)
    ### 카트 내용을 정렬: delivery 기준으로 먼저 정렬하고, 그 다음 packaging 기준으로 정렬
    sorted_cart = sorted(cart, key=lambda item: (item['product'].delivery, item['product'].packaging))

    return render(request, 'cart/detail.html', {'cart': cart, 'sorted_cart': sorted_cart, 'categories': categories})
