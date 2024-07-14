from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, ProductImage, Category, Stock

# Register your models here.

admin.site.unregister(Group)
# admin site setup
admin.site.site_header = 'E-Store Administration'
admin.site.site_title = 'E-Store'

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
    list_display = ["name", "active"]
    list_editable = ["active"]
    list_per_page = 10
    inlines = [ProductImageInline, StockInline]
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["cat_name",]



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
