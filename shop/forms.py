from django import forms

# 상품리스트 필터링을 위한 폼
class ProductFilterForm(forms.Form):
    delivery = forms.ChoiceField(
        choices=[(None,'-----'), ('샛별배송', '샛별배송'), ('하루배송', '하루배송'), ('판매자배송', '판매자배송')],
        required=False,  # 선택 필드로 설정
        label="배송 방식"
    )

    packaging = forms.ChoiceField(
        choices=[(None,'-----'), ('상온', '상온'), ('냉장', '냉장'), ('냉동', '냉동')],
        required=False,  # 선택 필드로 설정
        label="포장 방식"
    )

    min_price = forms.IntegerField(min_value=0, required=False, label="최소 가격", initial=0)
    max_price = forms.IntegerField(min_value=0, required=False, label="최대 가격")

    array = forms.ChoiceField(
        choices=[(None,'-----'), ('낮은가격', '낮은가격부터'), ('높은가격', '높은가격부터')],
        required=False,  # 선택 필드로 설정
        label="가격 순서"
    )
    
    




