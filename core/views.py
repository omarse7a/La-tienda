from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category

# Create your views here.
def index(request):
    return render(request, "home.html")


# Product related views
def product_list(request, cat_name):
    categories = Category.objects.all() # get all categories from db

    # Filter by selected category
    if cat_name == "all":
        products = Product.objects.all()  # Get all products from db
    else:
        category = Category.objects.get(cat_name=cat_name)
        products = category.get_cat_products()  # get all products by this category
    
    context = {
                "products": products, 
                "categories": categories,
                "selected_cat": cat_name, 
               }
    return render(request, "products/product_list.html", context)

def product_search(request):
    categories = Category.objects.all()  # Get all categories from db

    # Search functionality
    search_value = request.GET.get("search-inp", "")
    if search_value:
        products = Product.objects.filter(
            Q(name__icontains=search_value) | Q(category__cat_name__startswith=search_value)
        )
        selected_cat = f"results for '{search_value}'"
    else:
        products = Product.objects.all()  # Get all products from db
        selected_cat = "all"
    
    context = {
                "products": products, 
                "categories": categories,
                "selected_cat": selected_cat, 
               }
    return render(request, "products/product_list.html", context)