from django.db import models
from product_models import Product

################ Bag and payment related models ################

class Bag(models.Model):
    session_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.session_key}"
    
class BagItem(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def item_subtotal(self):
        return self.quantity * self.product.price