from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
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
            'similar_products': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('price', css_class='form-control'),
            Field('currency', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('recomended_title', css_class='form-control'),
            Field('recomended_text', css_class='form-control'),
            Field('subsubcategory', css_class='form-control'),
            Field('similar_products', css_class='form-control'),
            Submit('submit', 'Save Product', css_class='btn btn-primary')
        )


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'