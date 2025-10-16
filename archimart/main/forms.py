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

        if self.instance and self.instance.pk:
            # Exclude the product itself, but allow all others
            self.fields["similar_products"].queryset = Product.objects.exclude(pk=self.instance.pk)
        else:
            self.fields["similar_products"].queryset = Product.objects.all()


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'

class ProductColorForm(forms.ModelForm):
    class Meta:
        model = Product_Color
        fields = '__all__'