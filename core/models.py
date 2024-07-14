from django.db import models
from django.utils.text import slugify

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

    FITS = [
        ('regular_fit', 'Regular Fit'),
        ('relaxed_fit', 'Relaxed Fit'),
        ('slim_fit', 'Slim Fit'),
    ]

    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    fit = models.CharField(max_length=255, choices=FITS, default="regular_fit")
    category = models.ForeignKey(Category, null=True, related_name='products', on_delete=models.SET_NULL)
    main_image = models.ImageField(upload_to='product-images/%y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="name in URL")
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
     
    def get_images(self):
        return self.images.all()
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        #  # initialize stock for all sizes
        # sizes = [choice[0] for choice in Stock.SIZE_CHOICES]
        # for size in sizes:
        #     Stock.objects.get_or_create(product=self, size=size)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images/%y/%m/%d')

    def __str__(self):
        return f"Image for {self.product.name}"
    

class Stock(models.Model):
    SIZE_CHOICES = [
        ("X-Small", "XS"),
        ("Small", "S"),
        ("Medium","M"),
        ("Large", "L"),
        ("X-Large", "XL"),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} Pieces of {self.product.name} - Size: {self.size}"

    class Meta:
        unique_together = ('product', 'size')
        ordering = ['product',]
        indexes = [
            models.Index(fields=['product', 'size']),
        ]
