from django.db import models

# Create your models here.

class Category(models.Model):
    cat_name = models.CharField(max_length=255, unique=True, verbose_name="category name")

    def __str__(self):
        return self.cat_name
    
    def get_cat_products(self):
        return self.products.all()
    
    class Meta:
        verbose_name_plural = "Categories"
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    fit = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, null=True, related_name='products', on_delete=models.SET_NULL)
    main_image = models.ImageField(upload_to='product-images/%y/%m/%d')

    def __str__(self):
        return self.name
    
    def get_images(self):
        return self.images.all()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images/%y/%m/%d')

    def __str__(self):
        return f"Image for {self.product.name}"
    

    
class Stock(models.Model):
    SIZE_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("32", "32"),
        ("34", "34"),
        ("36", "36"),
        ("38", "38"),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} Pieces of {self.product.name} - Size: {self.size}"

    class Meta:
        unique_together = ('product', 'size')
        indexes = [
            models.Index(fields=['product', 'size']),
        ]
