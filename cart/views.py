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
    cart = Cart(request)
    ### 카트 내용을 정렬: delivery 기준으로 먼저 정렬하고, 그 다음 packaging 기준으로 정렬
    sorted_cart = sorted(cart, key=lambda item: (item['product'].delivery, item['product'].packaging))

    return render(request, 'cart/detail.html', {'cart': cart, 'sorted_cart': sorted_cart})





    # grouped_items = defaultdict(lambda: defaultdict(list))  # delivery와 packaging을 기준으로 그룹화

    # ### 카트 내 상품들을 반복
    # for item in cart:
    #     product = item['product']
    #     # 상품을 delivery -> packaging 방식으로 그룹화
    #     grouped_items[product.delivery][product.packaging].append(item)

    # print(grouped_items)  # 디버그용 출력

    # ### 그룹화된 데이터를 템플릿으로 넘김
    # return render(request, 'cart/detail.html', {
    #     'cart': cart,
    #     'grouped_items': grouped_items,  # 그룹화된 아이템 전달
    #     })
        




    # for item in cart: #초기화한 후 아이템의 정보를 재구성해서 보여준다
    #     item['updated_quantity_form'] = CartAddProductForm(initial={
    #                                         'quantity': item['quantity'],
    #                                         'override': True
    #                                     })

    # how_many_types = cart.__len__ ### 카트 속 상품 숫자

    # return render(request, 'cart/detail.html', {'cart': cart, 'types': how_many_types})














'''
defaultdict(<function cart_detail.<locals>.<lambda> at 0x00000162270A5120>, {
    '샛별배송': defaultdict(<class 'list'>, {
    '냉장': [{'quantity': 2, 'price': Decimal('7000'), 'product': <Product: 달걀 한 판>, 'total_price': Decimal('14000')}, {'quantity': 4, 'price': Decimal('10000'), 'product': <Product: 사과 한 상자>, 'total_price': Decimal('40000')}]})})

'''