from django.shortcuts import render
from .models import Product, Category

# Create your views here.
def index(request):
    return render(request, "home.html")

def product_list(request, cat_name):
    products = Product.objects.all()
    categories = Category.objects.all()

    if cat_name:
        if cat_name != 'all':
            category = Category.objects.get(cat_name=cat_name)
            products = products.filter(category=category)
            # products = category.get_cat_products()
    
    context = {
                "products": products, 
                "categories": categories,
                "selected_cat": cat_name, 
               }
    return render(request, "product_list.html", context)