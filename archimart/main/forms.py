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
        fields = "__all__"
        widgets = {
            "similar_products": forms.SelectMultiple(
                attrs={"class": "dual-listbox", "size": "10"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Leave queryset empty initially; populate via AJAX
        self.fields["similar_products"].queryset = Product.objects.none()


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'