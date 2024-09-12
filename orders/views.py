from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .models import Order, Ordereditem
from .forms import ProductForm
from cart.cart import Cart
from shop.models import Product, Category


# 주문 처리
def order_create(request):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return HttpResponse('먼저 로그인 해주시길 바랍니다.')

    # 장바구니 세션 정보 가져오기
    cart = Cart(request)

    # 세션에 장바구니에 담긴 물품이 없을 경우
    if len(cart) == 0:
        return HttpResponse('장바구니에 물품이 없습니다.')

    # 주문 생성
    order = Order.objects.create(
        customer=request.user,  # 로그인한 사용자 정보
        order_cost=cart.get_total_price(),  # 장바구니의 총 가격
        deliver_address=request.user.address  # 유저 모델에서 주소 정보를 가져옴
    )

    # 주문 항목 생성
    for item in cart:
        product = item['product']
        Ordereditem.objects.create(
            order=order,
            product=item['product'],
            order_price=item['price'],
            order_quantity=item['quantity']
        )
        # 재고 감소
        product.stock -= item['quantity']  # 주문한 수량만큼 재고를 줄임
        product.save()  # 재고를 데이터베이스에 저장

    # 장바구니 비우기
    cart.clear()

    # 주문 완료 페이지로 이동
    return render(request, 'orders/order_succeeded.html', {'order': order})

# 상품 등록
def product_create(request):
    if not request.user.is_authenticated:
        return redirect('login')  # 로그인하지 않은 경우 로그인 페이지로 리다이렉트
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES) #이미지 저장을 위해 필요
        if form.is_valid():
            form.save()
            return redirect('orders:product_seller', username=request.user.name)
    else:
        form = ProductForm(initial={'seller': request.user.name})
    
    return render(request, 'orders/product_create.html', {'form': form})

# 내 상품 화면
def product_seller(request, username):
    products = Product.objects.filter(seller=username)

    context = {
        'products': products,
    }
    return render(request, 'orders/product_seller.html', context)


# 상품 삭제
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.user.name == product.seller:
        product.delete()
        return JsonResponse({'status': 'success'})  # 성공 시 JSON 응답
    
    return JsonResponse({'status': 'error', 'message': '삭제 권한이 없습니다'}, status=403)  # 실패 시 JSON 응답

# 상품 정보 수정
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('orders:product_seller', username=request.user.name)
    else:
        form = ProductForm(instance=product)
        return render(request, 'orders/product_form.html', {'form': form})
    

# 판매자가 상품 구매 내역 확인
def sold_history(request):
    # 판매자가 등록한 상품
    seller_products = Product.objects.filter(seller=request.user.name)
    # 등록한 상품 중 주문되었던 것을 가져옴
    order_items = Ordereditem.objects.filter(product__in=seller_products).select_related('order', 'product')
    
    context = {
        'order_items': order_items,
    }
    
    return render(request, 'orders/sold_history.html', context)

# 주문 내역
def order_history(request):
    if not request.user.is_authenticated:
        return redirect('users:login')  # 로그인하지 않은 경우 로그인 페이지로 리다이렉트

    # 사용자의 주문 목록
    orders = Order.objects.filter(customer=request.user)

    context = {
        'orders': orders,
    }

    return render(request, 'orders/order_history.html', context)
