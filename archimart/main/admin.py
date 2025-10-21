from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(SubSubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Specification)
admin.site.register(Product_Color)
admin.site.register(Product_Size)
admin.site.register(Product_Thickness)