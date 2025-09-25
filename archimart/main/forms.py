from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django_select2.forms import Select2MultipleWidget
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'


class SubSubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubSubCategory
        fields = '__all__'



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'currency',
            'description',
            'recomended_title',
            'recomended_text',
            'subsubcategory',
            'similar_products',
        ]
        widgets = {
            'similar_products': Select2MultipleWidget(attrs={'class': 'form-control'}),
        }
    # Rest of the form (FormHelper, etc.) remains the same


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'