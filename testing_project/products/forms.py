from django import forms
from .models import Product

"""
form에서 각 필드의 유효성 검사
- form.is_valid()를 호출하면 Django는 각 폼 필드에 대해 clean_<field_name> 메서드를 호출
- 그래서 각 필드에 대한 유효성검사를 작성하고 싶다면, form 안에 clean_<field_name>를 오버라이딩하면 된다.
"""

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'stock_count')

    def clean_price(self):
        """ price필드에 대한 유효성검사 """
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('Price cannot be negative')
        return price

    def clean_stock_count(self):
        """ stock_count필드에 대한 유효성검사 """
        stock_count = self.cleaned_data.get('stock_count')
        if stock_count < 0:
            raise forms.ValidationError('stock_count cannot be negative')
        return stock_count