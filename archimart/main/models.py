from django.db import models
from django_resized import ResizedImageField
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[500,500],quality=85,upload_to="Category",verbose_name="Category Image",null=True,blank=True)
    def __str__(self):
        return self.name 
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = ResizedImageField(size=[500,500],quality=85,upload_to="SubCategory",verbose_name="Sub Category Image",null=True,blank=True)
    def __str__(self):
        return f"{self.name} --> {self.category.name}"
    

class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    image = ResizedImageField(size=[500,500],quality=85,upload_to="SubSubCategory",verbose_name="Sub Sub Image",null=True,blank=True)
    def __str__(self):
        return f"{self.name} --> {self.subcategory.name}"

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    currency = models.CharField(max_length=50,choices=(
        ('BDT','BDT'),
        ('USD','USD'),
        ('INR','INR'),
    ),default='BDT')
    description = models.TextField()
    # category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category")
    # subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='subcategory')
    subsubcategory = models.ForeignKey(SubSubCategory,on_delete=models.CASCADE,related_name='subsubcategory')
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image")
    def __str__(self):
        return f"{self.product.name} image"
    
class Specification(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.key} --> {self.value} --> {self.product.name}"
    

