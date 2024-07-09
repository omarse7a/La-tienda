from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category

# Create your views here.
def index(request):
    return render(request, "home.html")


# Product related views
def product_list(request, cat_name):
    products = Product.objects.all()    # get all products from db
    categories = Category.objects.all() # get all categories from db

    # Filter by selected category
    if cat_name != "all":
        category = Category.objects.get(cat_name=cat_name)
        products = category.get_cat_products()  # get all products by this category
    
    context = {
                "products": products, 
                "categories": categories,
                "selected_cat": cat_name, 
               }
    return render(request, "product_list.html", context)

def product_search(request):
    products = Product.objects.all()    # get all products from db
    categories = Category.objects.all() # get all categories from db

    # Search functionality
    search_value = request.GET.get("search-inp")
    if search_value:
        products = products.filter( Q(name__icontains=search_value) | Q(category__cat_name__startswith=search_value))
    
    context = {
                "products": products, 
                "categories": categories,
                "selected_cat": f"results for '{search_value}'", 
               }
    return render(request, "product_list.html", context)