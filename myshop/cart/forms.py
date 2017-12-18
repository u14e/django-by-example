from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,   # 将输入的值转换为int
                                      empty_value=0)
    update = forms.BooleanField(required=False,
                                initial=False,  # False: add, True: update
                                widget=forms.HiddenInput)
