from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, ProductImage, Category, Stock

# Register your models here.

admin.site.unregister(Group)

admin.site.site_header = 'E-Store'
admin.site.site_title = 'E-Store'

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name",]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Stock)