from typing import Any
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models.product_models import Product, ProductImage, Category, Stock
from .models.bag_models import Bag, BagItem,ShippingInfo

################ Product management admin models ################

admin.site.unregister(Group)
# admin site setup
admin.site.site_header = 'La tienda Administration'
admin.site.site_title = 'La tienda'

# product image inline to be added with the product
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

# product stock inline to be added with the product
class StockInline(admin.TabularInline):
    model = Stock
    extra = 0
    # creating extra fields for stocks when adding a product
    def get_extra(self, request, obj=None, *args, **kwargs):
        if obj: # if the product exists don't create extra fields
            return 0
        return len(Stock.SIZE_CHOICES) # if the product is new create a stock field for each size


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "active"]
    list_editable = ["active"]
    list_filter = ["category", "active"]
    search_fields = ["name"]
    list_per_page = 10
    inlines = [ProductImageInline, StockInline]
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["cat_name",]

################ Order management admin models ################

class OrderItemInline(admin.TabularInline):
        model = BagItem
        extra = 0
        def get_readonly_fields(self, request, obj=None):
            return ["product", "size", "quantity"]

class ShippingInfoInline(admin.StackedInline):
    model = ShippingInfo
    extra = 0

# tracking orders in admin panel using the Bag model
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_display", "session_key", "delivered", "bag_items_num", "bag_total"]
    list_editable = ["delivered"]
    fields = ["order_date", "ordered", "delivered", "bag_items_num", "bag_total"]
    readonly_fields = ["order_date", "ordered", "bag_items_num", "bag_total"]
    inlines = [OrderItemInline, ShippingInfoInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(ordered = True)
    
    def order_display(self, obj):
        return str(obj)
    order_display.short_description = "Order ID"

    def bag_items_num(self, obj):
        return obj.bag_items_num
    
    def bag_total(self, obj):
        return obj.bag_total


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bag, OrderAdmin)

# admin.site.register(Bag)
# admin.site.register(BagItem)
# admin.site.register(ShippingInfo)
