from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# 카테고리
class Category(models.Model):
    ### slug가 한글로 된 카테고리 따라오지 못하는 현상 발생 -> db 'name'필드와 출력값을 구분함.
    NAME = [
        ('vegetable','채소'),
        ('fruits-nuts-rice', '과일·견과·쌀'),
        ('meat-eggs','정육·가공육·계란'),
        ('water-beverages','생수·음료'),
        ('furniture-interior','가구·인테리어'),
        ('pet','반려동물'),
    ]

    name = models.CharField(max_length=200, choices=NAME)
    slug = models.SlugField(max_length=200, unique=True)

    ### 상기한 한글 이슈 -> slug값에 db 'name'필드의 값을 지정해서 저장
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name'] # 'name'순서 정렬
        indexes = [
            models.Index(fields=['name']), # 'name' 인덱스
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self): # 카테고리 이름을 문자열로 출력
        return self.name

    
    def get_absolute_url(self): # 절대경로 설정
        return reverse('shop:product_list_by_category', args=[self.slug])


### SubCategory를 만들면?
### parent = models.ForeignKey(Category, blank=True, related_name='children')
### 아마도 Product.category 의 ForeignKey 참조 영역을 바꿔야할수도?(셀프참조를 쓰면 해결?)


# 상품
class Product(models.Model):
    DELIVERY = [ # 배송방식
        ('샛별배송', '샛별배송'),
        ('판매자배송', '판매자배송'),
        #설치배송
    ]
    PACKAGING = [   # 포장방식
        ('상온', '상온'),
        ('냉장', '냉장'),
        ('냉동', '냉동'),
    ]

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200) 
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=0) # 원(단위)
    available = models.BooleanField(default=True) #제품판매가 가능한지 아닌지 여부
    delivery = models.CharField(max_length=10, choices=DELIVERY)
    packaging = models.CharField(max_length=10, choices=PACKAGING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    # 판매자
    # 중량/용량
    # 알레르기정보
    # 소비기한

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):  # 상품명 문자열로 출력
        return self.name

    def get_absolute_url(self): # 절대경로
        return reverse('shop:product_detail', args=[self.id, self.slug])
