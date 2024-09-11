from cart.cart import Cart

def cart_item_count(request):
    cart = Cart(request)
    return {
        'cart_item_count': len(cart)  # 카트에 담긴 상품 종류 수 반환
    }