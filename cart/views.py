from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from shop.models import Product
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


#카트 표현부분
def cart_detail(request):
    cart = Cart(request)

    for item in cart: #초기화한 후 아이템의 정보를 재구성해서 보여준다
        item['updated_quantity_form'] = CartAddProductForm(initial={
                                            'quantity': item['quantity'],
                                            'override': True
                                        }) 

    return render(request, 'cart/detail.html', {'cart': cart})

