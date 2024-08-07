from dal import autocomplete
from django import forms
from .models import ProductAttribute

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = '__all__'
        widgets = {
            'option': autocomplete.ModelSelect2(url='option-autocomplete', forward=['attribute'], attrs={
                'data-placeholder': 'Выберите опцию',
                'data-minimum-input-length': 0,
                'data-minimum-results-for-search': 'Infinity',  # Отключение поиска
            })
        }
