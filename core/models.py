from django.db import models
from django.utils.text import slugify

################ Product related models ################

class Category(models.Model):
    cat_name = models.CharField(max_length=255, unique=True, verbose_name="category name")

    def __str__(self):
        return self.cat_name
    
    @property
    def cat_products(self):
        return self.products.all()
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['cat_name']
    
class Product(models.Model):

    FITS = [
        ('Regular Fit', 'regular_fit'),
        ('Slim Fit', 'slim_fit'),
        ('Relaxed Fit', 'relaxed_fit'),
    ]


    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    fit = models.CharField(max_length=255, choices=FITS, default="Regular Fit")
    category = models.ForeignKey(Category, null=True, related_name='products', on_delete=models.SET_NULL)
    main_image = models.ImageField(upload_to='product-images/%y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="name in URL")
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def images(self):
        return self.productimage_set.all()
    
    @property
    def image_count(self):
        return self.productimage_set.count()
    
    class Meta:
        ordering = ["active", "created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
        ]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images/%y/%m/%d')

    def __str__(self):
        return f"Image for {self.product.name}"
    
    class Meta:
        ordering = ['product']
    

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

################ Bag and payment related models ################

