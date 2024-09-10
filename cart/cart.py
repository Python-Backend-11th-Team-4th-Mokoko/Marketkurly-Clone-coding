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


