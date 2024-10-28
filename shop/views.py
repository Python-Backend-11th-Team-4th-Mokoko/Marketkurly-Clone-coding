from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from shop.models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from shop.forms import ProductFilterForm

### 홈 페이지
def home_page(request):
    categories = Category.objects.all()
    # 랜덤하게 4개의 상품을 가져옴
    products = Product.objects.filter(available=True).order_by('?')[:4]
    all_products = Product.objects.all()

    return render(request, 'shop/home.html', 
                  {'categories': categories, 'products': products, 
                   'all_products': all_products})


# 상품 리스트
def product_list(request, category_slug=None):
    all_products = Product.objects.all()
    category = None # 안정성을 위해 None 할당
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()

    #카테고리별로 확인
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug) # slug값을 받아 카테고리 선별
        products = products.filter(category=category) # 선별한 카테고리의 상품

    ### 조건별로 상품을 필터링
    if request.method == 'POST':
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            # 배송방식 필터링
            delivery = form.cleaned_data.get('delivery')
            if delivery:
                products = products.filter(delivery=delivery)

            # 포장방식 필터링
            packaging = form.cleaned_data.get('packaging')
            if packaging:
                products = products.filter(packaging=packaging)

            # 가격 필터링
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            if min_price is not None:
                products = products.filter(price__gte=min_price)
            if max_price is not None:
                products = products.filter(price__lte=max_price)

            # 가격 순서 정렬
            array = form.cleaned_data.get('array')
            if array == '낮은가격':
                products = products.order_by('price')  # 가격 오름차순
            elif array == '높은가격':
                products = products.order_by('-price')  # 가격 내림차순
            
            form.clean()
    else:
        form = ProductFilterForm()

    # 카테고리, 모든 카테고리, 상품 정보를 보내 렌더링
    return render(request, 'shop/product/list.html',
                  {'category': category, 'categories': categories, 
                   'products': products, 'cart_product_form': cart_product_form,
                   'form': form, 'all_products': all_products})

@login_required
def list_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            # 폼에서 수량을 가져와 장바구니에 추가
            quantity = form.cleaned_data['quantity']
            cart = Cart(request)  # 세션 기반 Cart 객체 가져오기
            cart.add(product=product, quantity=quantity)  # 장바구니에 추가
            cart.save()  # 세션 저장

        return redirect('shop:product_list')  # 상품 리스트 페이지로 리디렉션
    else:
        form = CartAddProductForm(initial={'quantity': 1})  # 기본 수량 1로 초기화된 폼 반환
    return redirect('shop:product_list')


### 신상품
def new_products(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()
    one_week_ago = timezone.now() - timedelta(days=7) # 1주일 이내의 상품만
    new_products = Product.objects.filter(available=True, created__gte=one_week_ago).order_by('-created') #최신상품 순으로 정렬

    ### 조건별로 상품을 필터링
    form = ProductFilterForm(request.GET)
    if form.is_valid():
        # 배송방식 필터링
        delivery = form.cleaned_data.get('delivery')
        if delivery:
            new_products = new_products.filter(delivery=delivery)
        # 포장방식 필터링
        packaging = form.cleaned_data.get('packaging')
        if packaging:
            new_products = new_products.filter(packaging=packaging)
        # 가격 필터링
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        if min_price is not None:
            new_products = new_products.filter(price__gte=min_price)
        if max_price is not None:
            new_products = new_products.filter(price__lte=max_price)
        # 가격 순서 정렬
        array = form.cleaned_data.get('array')
        if array == '낮은가격':
            new_products = new_products.order_by('price')  # 가격 오름차순
        elif array == '높은가격':
            new_products = new_products.order_by('-price')  # 가격 내림차순
        
    return render(request, 'shop/product/new_products.html', 
                  {'categories': categories, 'new_products': new_products, 'form': form, 'all_products': all_products})



# 상품 정보
def product_detail(request, id, slug):
    all_products = Product.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    total_price = product.price
    updated_quantity = None

    ### 상품 상세 화면에서 변동하는 가격을 즉시 표시해주기 위한 기능, 장바구니로 담는 기능
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            if request.POST.get('action') == '+':
                form.add_quantity(request)
            elif request.POST.get('action') == '-':
                form.subtract_quantity(request)

            quantity = form.cleaned_data['quantity']  # 입력된 수량
            total_price = product.price * quantity  # 총 가격 계산

            # 수량 변경 후 폼의 값을 업데이트
            updated_quantity = form.cleaned_data['quantity']
            form = CartAddProductForm(initial={'quantity': updated_quantity})

            if request.POST.get('action') == 'add_to_cart':
                cart = Cart(request)  # Cart 객체 생성 (세션 기반)
                product_id = request.POST.get('product_id')  # 폼에서 넘어온 상품 ID 가져오기
                cart.add(product=product, quantity=updated_quantity)  # 장바구니에 상품 추가
                cart.save()  # 세션 저장
                
    else:
        form = CartAddProductForm()
    ###

    # 상품정보를 보내 렌더링
    return render(request, 'shop/product/detail.html',
                  {'product': product, 'cart_product_form': form, 
                   'total_price': total_price, 'updated_quantity': updated_quantity, 
                   'all_products': all_products})


model = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 검색기능
def search_products(request):
    query = request.GET.get('q', '')

    if query:
        # 모든 상품 정보 가져오기
        products = Product.objects.all()

        # 각 상품의 이름과 설명을 결합한 텍스트 생성
        # 상품 텍스트 결합 시, 상품명을 두 번 포함하여 가중치 부여
        product_texts = [f"{product.product_name} {product.product_name} {product.description}" for product in products]

        # 상품 텍스트 임베딩 생성
        product_embeddings = model.encode(product_texts)

        # 사용자 검색어 임베딩 생성
        query_embedding = model.encode([query])

        # 유사도 계산 (코사인 유사도)
        similarities = cosine_similarity(query_embedding, product_embeddings)[0]

        # 유사도 정보와 함께 상품을 정렬
        products_with_similarity = sorted(zip(products, similarities), key=lambda x: x[1], reverse=True)

        # 유사도가 높은 상위 N개의 상품 반환
        results = [product for product, similarity in products_with_similarity if similarity > 0.3]  # 유사도가 0.3 이상인 상품만

    else:
        results = []

    ### 조건별로 상품을 필터링
    if request.method == 'POST':
        form = ProductFilterForm(request.POST)
        if form.is_valid():
            filtered_results = results

            # 배송방식 필터링
            delivery = form.cleaned_data.get('delivery')
            if delivery:
                filtered_results = [product for product in filtered_results if product.delivery == delivery]

            # 포장방식 필터링
            packaging = form.cleaned_data.get('packaging')
            if packaging:
                filtered_results = [product for product in filtered_results if product.packaging == packaging]

            # 가격 필터링
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            if min_price is not None:
                filtered_results = [product for product in filtered_results if product.price >= min_price]
            if max_price is not None:
                filtered_results = [product for product in filtered_results if product.price <= max_price]

            # 가격 순서 정렬
            array = form.cleaned_data.get('array')
            if array == '낮은가격':
                filtered_results = sorted(filtered_results, key=lambda product: product.price)  # 가격 오름차순
            elif array == '높은가격':
                filtered_results = sorted(filtered_results, key=lambda product: product.price, reverse=True)  # 가격 내림차순

            # 필터링된 결과로 업데이트
            results = filtered_results

    else:
        form = ProductFilterForm()

    return render(request, 'shop/product/search_results.html', {'results': results, 'query': query, 'form': form})
