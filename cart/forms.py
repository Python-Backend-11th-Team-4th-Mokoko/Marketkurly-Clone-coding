from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1) 
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput) # 오버라이드

    # 수량 선택
    def add_quantity(self, request):
        self.cleaned_data['quantity'] += 1

    def subtract_quantity(self, request):
        if self.cleaned_data['quantity'] > 1:
            self.cleaned_data['quantity'] -= 1
    


    #장바구니에서 선택하는 기능? (여기에 넣는게 맞는것인가?)
    # is_selected = forms.BooleanField(required=False, initial=False)

