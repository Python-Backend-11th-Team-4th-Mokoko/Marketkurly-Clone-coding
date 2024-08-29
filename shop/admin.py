from django.contrib import admin

from shop.models import Category, Product

# Register your models here.

@admin.register(Category)
class CetegoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # 자동완성 영역

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'delivery', 'packaging', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'delivery']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

