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
    discount = models.FloatField(default=0)
    currency = models.CharField(max_length=50,choices=(
        ('BDT','BDT'),
        ('USD','USD'),
        ('INR','INR'),
    ),default='BDT')
    description = models.TextField()
    recomended_title = models.CharField(max_length=100,null=True,blank=True,verbose_name="ArchiMart Recomendation Title")
    recomended_text = models.TextField(null=True,blank=True,verbose_name="ArchiMart Recomendation Text")
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.CASCADE, related_name='products')
    image1 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True)
    image2 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True)
    image3 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True)
    # Self-referential ManyToMany
    Specification = models.TextField(null=True,blank=True)
    similar_products = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="related_to"
    )
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image")
    def __str__(self):
        return f"{self.product.name} image"
    
class Specification(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    key = models.CharField(max_length=50,choices=(('Weight','Weight'),('Dimensions','Dimensions'),('Size','Size'),('Color','Color'),('Material','Material'),('Other','Other')),default='Other')
    value = models.CharField(max_length=100)
    price = models.IntegerField(default=0,null=True,blank=True)
    image = ResizedImageField(size=[700,700],quality=85,upload_to="Specification",verbose_name="Specification Image",null=True,blank=True)

    def __str__(self):
        return f"{self.key} --> {self.value} --> {self.product.name}"
    

class Product_Color(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    image1 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True)
    image2 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True)
    image3 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True)

    def __str__(self):
        return f"{self.Product.name} --> {self.color}"

class Product_Size(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    image1 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image")
    image2 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True)
    image3 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True) 
    def __str__(self):
        return f"{self.Product.name} --> {self.size}"
    
class Product_Thickness(models.Model):
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    thickness = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    image1 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image")
    image2 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True)
    image3 = ResizedImageField(size=[700,700],quality=85,upload_to="Product",verbose_name="Product Image",null=True,blank=True) 
    def __str__(self):
        return f"{self.Product.name} --> {self.thickness}"
    


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    customer_email = models.EmailField(null=True, blank=True)
    pay_method = models.CharField(max_length=50, choices=(
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Online Payment', 'Online Payment'),
    ), default='Cash on Delivery')
    transection_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, choices=(
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ), default='Pending')
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    invoice = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    thickness = models.CharField(max_length=50, null=True, blank=True)
    price = models.FloatField(default=0)

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} × {self.quantity} ({self.order.customer_name})"
