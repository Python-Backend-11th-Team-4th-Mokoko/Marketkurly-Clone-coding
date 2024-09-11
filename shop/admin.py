from django.contrib import admin

from shop.models import Category, Product

# Register your models here.

@admin.register(Category)
class CetegoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'product_name', 'slug', 'price', 'stock', 'available', 'delivery', 'packaging', 'seller', 'created', 'updated']
    list_filter = ['stock', 'available', 'seller', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('product_name',)} # 자동완성 영역