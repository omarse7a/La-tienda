from typing import Iterable
from django.utils import timezone
from django.db import models
from django.forms import ValidationError
from .product_models import Product, Stock

################ Bag and Checkout models ################

class Bag(models.Model):
    session_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(null=True, blank=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"

    # returns all bag items as a list
    @property
    def bag_items(self):
        return self.bagitem_set.all()
    # returns the number all bag items as int
    @property
    def bag_items_num(self):
        return sum(item.quantity  for item in self.bagitem_set.all())
    # returns the total price of all bag items
    @property
    def bag_total(self):
        return sum(item.item_subtotal for item in self.bagitem_set.all())
    
    # creates a bag item or increment an existing one
    def add_item(self, product, size):
        item, created = BagItem.objects.get_or_create(bag=self, product=product, size=size)
        if not created:
            item.quantity += 1
            item.save()

    # removes a bag item
    def remove_item(self, product, size):
        try:
            item = BagItem.objects.get(bag=self, product=product, size=size)
            item.delete()
        except BagItem.DoesNotExist:
            pass
    
    # updates bag item's quantity
    def update_item(self, product, size, quantity=1):
        try:
            item = BagItem.objects.get(bag=self, product=product, size=size)
            item.quantity = quantity
            item.save()
        except BagItem.DoesNotExist:
            pass

    # confirms the order (make it appear in order in the admin panel)
    def mark_as_ordered(self, shipping_info):
        self.ordered = True
        self.order_date = timezone.now()
        shipping_info.bag = self
        shipping_info.save()
        self.save()
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["delivered","order_date"]


class BagItem(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    size = models.CharField(max_length=20, choices=Stock.SIZE_CHOICES, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} pieces of {self.size} {self.product.name}"
    
    # calc the subtotal for each item
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

    # decrease the stock quantity when the order is confirmed
    def deallocate_stock(self):
        available_stock = Stock.objects.get(product=self.product, size=self.size)
        available_stock.decrease_stock(self.quantity)
    
    class Meta:
        verbose_name_plural = "items"


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
    address = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    bag = models.OneToOneField(Bag, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.governorate}"
    
