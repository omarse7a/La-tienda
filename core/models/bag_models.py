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
        return self.bagitem_set

    @property
    def bag_total(self):
        return sum(item.item_subtotal for item in self.bagitem_set)
    
    def add_item(self):
        pass

    def remove_item(self):
        pass
    
class BagItem(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    size = models.CharField(max_length=20, choices=Stock.SIZE_CHOICES)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} pieces of {self.product.name}"
    
    @property
    def item_subtotal(self):
        return self.quantity * self.product.price
    
    def increase_quantity(self):
        self.quantity += 1
        available_stock = Stock.objects.get(product=self.product, size=self.size)
        available_stock.decrease_stock(1)

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            available_stock = Stock.objects.get(product=self.product, size=self.size)
            available_stock.increase_stock(1)
        else: # you can remove product
            raise ValidationError("Cannot decrease the quantity than 1")


