from django.utils import timezone
from django.db import models
from django.forms import ValidationError
from .product_models import Product, Stock

################ Bag and Checkout models ################

class ShippingInfo(models.Model):
    GOVS = [
        ("cairo", "Cairo"),
        ("giza", "Giza"),
        ("alexandria", "Alexandria"),
        ("north_coast", "North Coast"),
    ]
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(max_length=255)
    customer_number = models.CharField(max_length=255)
    governorate = models.CharField(max_length=255, choices=GOVS)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building_no = models.PositiveSmallIntegerField()
    landmark = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.building_no} {self.street}, {self.city}, {self.governorate}"
    

class Bag(models.Model):
    session_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(null=True, blank=True)
    shipping_info = models.OneToOneField(ShippingInfo, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Bag {self.session_key}"

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
    
    def mark_as_ordered(self, shipping_info):
        self.ordered = True
        self.order_date = timezone.now()
        self.shipping_info = shipping_info
        self.save()

    def delete(self):
        if self.shipping_info:
            self.shipping_info.delete()
        return super().delete()


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
    
    # Checks availability for the items in the bag and adjust the quantities automatically
    def adjust_quantity(self):
        stock = Stock.objects.get(product=self.product, size=self.size)
        if self.quantity > stock.available_quantity:
            if not stock or stock.available_quantity == 0:
                self.delete()
                raise ValueError(f"{self.product.name} is out of stock. (We've removed it for you)")
            else:
                self.quantity = stock.available_quantity
                self.save()
                raise ValueError(f"The selected quantity is not available for {self.product.name}. (We've adjusted it for you)")
        self.save()
        # self.quantity = stock.decrease_stock(self.quantity)
        
    def reallocate_stock(self):
        available_stock = Stock.objects.get(product=self.product, size=self.size)
        available_stock.increase_stock(self.quantity)

    def deallocate_stock(self):
        available_stock = Stock.objects.get(product=self.product, size=self.size)
        available_stock.decrease_stock(self.quantity)

   