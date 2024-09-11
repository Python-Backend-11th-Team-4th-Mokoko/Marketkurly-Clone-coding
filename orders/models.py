from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from users.models import User
from shop.models import Product

# 주문 정보
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE) #외부키
    order_date = models.DateTimeField(auto_now_add=True)
    order_cost = models.DecimalField(max_digits=11, decimal_places=0) # 주문 당시 비용
    deliver_address = models.TextField(max_length=100)
    paid = models.BooleanField(default=False) # 결제 안된 상태에서 시작

    class Meta:
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['-order_date']),
        ]

    def __str__(self):
        return f'Order {self.id}'


# 주문아이템 정보
class Ordereditem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_price = models.DecimalField(max_digits=9, decimal_places=0) # 주문 당시 단가
    order_quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1, blank=False) # 주문한 수량

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.order_price * self.order_quantity
    
