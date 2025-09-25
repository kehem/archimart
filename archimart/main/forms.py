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
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name"),
            Field("price"),
            Field("currency"),
            Field("description"),
            Field("subsubcategory"),
            Field("similar_products", css_class="dual-listbox"),
            Submit("submit", "Save", css_class="btn btn-primary")
        )

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'