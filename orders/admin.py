from django.contrib import admin

from orders.models import Order, Ordereditem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = Ordereditem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_date', 'order_cost', 'deliver_address', 'paid')  # 관리자 페이지에서 보여줄 필드 설정
    list_filter = ('paid', 'order_date')
    inlines = [OrderItemInline]

