from shop.models import Category

def all_categories(request):
    category = Category.objects.all()
    return {
        'all_categories': category
    }
