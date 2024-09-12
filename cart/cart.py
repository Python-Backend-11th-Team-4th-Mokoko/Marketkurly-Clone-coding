from decimal import Decimal
from django.conf import settings
from django.shortcuts import redirect

from shop.models import Product

# 모델 대신 세션에 정보를 저장

class Cart:
    def __init__(self, request):
        self.session = request.session #세션정보를 멤버변수에
        cart = self.session.get(settings.CART_SESSION_ID) #세션정보 중 CART_SESSION_ID에 해당하는것
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {} #없으면 비어있는 카트 딕셔너리를 만들기

        self.cart = cart #지금까지 생성한 cart를 멤버변수화


    def add(self, product, quantity=1, override_quantity=False): #제품정보 추가 
        product_id = str(product.id)

        if product_id not in self.cart: #상품정보가 카트에 없으면 생성
           self.cart[product_id] = {'quantity': 0, 'price': str(product.price)} #self.cart에 새로 추가

        if override_quantity: #오버라이드가 True라면
            self.cart[product_id]['quantity'] = quantity
        else: #오버라이드가 False라면
            self.cart[product_id]['quantity'] += quantity

        self.save() #정보를 저장


    def save(self):
        self.session.modified = True #세션 객체가 수정되었음.


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart: #카트 속에 있을 경우
            del self.cart[product_id]
            self.save()

    ### 마켓컬리는 상품의 숫자가 아니라 카트에 담긴 종류의 숫자를 보여줌.
    def __len__(self): # 카트 내 담긴 상품의 종류 수를 반환
        return len(self.cart)
    
    # 카트에 포함된 아이템들을 반복해서 관련 Product 인스턴스에 접근해야 함. 이를 위해서 __iter__()정의
    def __iter__(self):
        product_ids = self.cart.keys() #카트속 상품들의 key를 전부 들고옴
        products = Product.objects.filter(id__in=product_ids) #__in 은 filter의 사용법 중 하나. 포함되어있는 것을 필터링한다(?)
        cart = self.cart.copy() #카트의 내용을 복사해서 가져옴

        for product in products:
            cart[str(product.id)]['product'] = product #product내용들을 id를 키로 해서 넣는다

        for item in cart.values():
            item['price'] = Decimal(item['price']) #기존의 가격값을 데시멀 형식으로 변경
            item['total_price'] = item['price']*item['quantity'] #각 품목별 가격총액

            yield item # 반복처리 가능한 item 자체가 반환됨(?)


    def get_total_price(self): #모든 품목의 가격 총액
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


# 그냥 메모용
# '''
# 이 __iter__ 메서드는 Django 프로젝트에서 장바구니(cart) 항목을 순회하고, 각 상품에 대한 세부 정보를 가공하여 반환하는 기능을 합니다. 이를 통해 장바구니에 담긴 항목들을 쉽게 처리할 수 있습니다. 주로 아래와 같은 상황에서 유용하게 사용됩니다:

# 1. 템플릿에서 장바구니 항목을 표시할 때
# 이터레이터는 for문을 사용하여 장바구니에 있는 상품들을 출력할 수 있도록 합니다. 예를 들어, 템플릿에서 장바구니에 담긴 상품을 하나씩 나열하면서 가격, 수량 등을 표시하고 싶을 때, __iter__를 통해 쉽게 데이터를 순회할 수 있습니다.

# python
# 코드 복사
# for item in cart:
#     print(item['product'], item['quantity'], item['total_price'])
# 2. 장바구니 내 총합 계산 및 처리
# 각 항목에 대해 개별 가격(price), 수량(quantity), 그리고 전체 가격(total_price)을 계산하여 반환하는 역할을 합니다. 이 값들은 총합을 계산하거나, 장바구니에서의 상품별 비용을 처리할 때 사용됩니다.

# 3. 장바구니 데이터를 복잡한 로직 없이 간편하게 사용
# 이터레이터는 장바구니의 데이터를 필요한 구조로 변환한 뒤 이를 한 번에 순회할 수 있는 장점을 제공합니다. 예를 들어, Decimal 형식으로 가격을 변환하고 각 상품의 합계를 계산한 뒤, 장바구니에 담긴 모든 데이터를 한꺼번에 처리할 수 있게 해줍니다.

# 4. 장바구니 정보를 JSON이나 API로 전달할 때
# 이터레이터를 사용하면 장바구니의 상품 목록을 간단하게 JSON으로 변환하거나 외부 API에 전달할 수 있습니다. 반환된 각 항목은 쉽게 처리할 수 있는 상태가 되므로, 다양한 로직에서 활용될 수 있습니다.

# 이 메서드는 장바구니의 모든 항목을 편리하게 처리하고, 가격 계산이나 수량 변경 같은 동작을 수행하기 위한 핵심 기능으로 작동합니다.
# '''
