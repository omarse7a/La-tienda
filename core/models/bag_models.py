from django.db import models
from django.forms import ValidationError
from .product_models import Product, Stock

################ Bag and payment related models ################

class Bag(models.Model):
    session_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.session_key}"

    @property
    def bag_items(self):
        return self.bagitem_set.all()
    
    @property
    def bag_items_num(self):
        return sum(item.quantity  for item in self.bagitem_set.all())

    @property
    def bag_total(self):
        return sum(item.item_subtotal for item in self.bagitem_set.all())
    
    def add_item(self, product, size):
        item, created = BagItem.objects.get_or_create(bag=self, product=product, size=size)
        if not created:
            item.quantity += 1
            item.save()

    def remove_item(self, product, size):
        try:
            item = BagItem.objects.get(bag=self, product=product, size=size)
            item.delete()
        except BagItem.DoesNotExist:
            pass
    def update_item(self, product, size, quantity=1):
        try:
            item = BagItem.objects.get(bag=self, product=product, size=size)
            item.quantity = quantity
            item.save()
        except BagItem.DoesNotExist:
            pass
    
class BagItem(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    size = models.CharField(max_length=20, choices=Stock.SIZE_CHOICES, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} pieces of {self.size} {self.product.name}"
    
    @property
    def item_subtotal(self):
        return self.quantity * self.product.price
    
    ########### could be deleted ###########
    # def increase_quantity(self):
    #     self.quantity += 1
    #     available_stock = Stock.objects.get(product=self.product, size=self.size)
    #     available_stock.decrease_stock(1)

    # def decrease_quantity(self):
    #     if self.quantity > 1:
    #         self.quantity -= 1
    #         available_stock = Stock.objects.get(product=self.product, size=self.size)
    #         available_stock.increase_stock(1)
    #     else: # i can make it remove product
    #         raise ValidationError("Cannot decrease the quantity than 1")

class ShippingInfo(models.Model):
    CITIES = [
        ("Cairo", "CAI"),
        ("Giza", "GIZ"),
        ("Alexandria", "ALX"),
        ("North Coast", "NC"),
    ]
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(max_length=255)
    customer_number = models.CharField(max_length=255)
    city = models.CharField(max_length=255, choices=CITIES)
    district = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building_no = models.PositiveSmallIntegerField()
    landmark = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.building_no} {self.street}, {self.district}, {self.city}"

   