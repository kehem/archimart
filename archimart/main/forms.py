from django import forms
from .models import *

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
            "name", "price", "currency", "description",
            "recomended_title", "recomended_text", "subsubcategory",
            "similar_products",
        ]
        widgets = {
            "similar_products": forms.SelectMultiple(
                attrs={"class": "duallistbox", "size": "10"}
            ),
        }

    def __init__(self, *args, **kwargs):
        # Expect instance when editing; helps exclude self and scope options
        super().__init__(*args, **kwargs)
        # Default queryset: all products
        qs = Product.objects.all()
        # Exclude self from selectable options
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            # Optional: scope to same subsubcategory for relevance
            if self.instance.subsubcategory_id:
                qs = qs.filter(subsubcategory_id=self.instance.subsubcategory_id)
        self.fields["similar_products"].queryset = qs
        # Optional: readable labels
        self.fields["similar_products"].label = "Similar products"

        
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'