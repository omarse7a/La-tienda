from django.shortcuts import render
from django.db.models import Q
from .models import Product, Category, Stock

# Create your views here.
def index(request):
    return render(request, "home.html")


# Product related views
def product_list(request, cat_name):
    categories = Category.objects.all() # get all categories from db

    # Filter by selected category
    if cat_name == "all":
        products = Product.objects.all()  # get all products from db
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
    categories = Category.objects.all()  # get all categories from db

    # Search functionality
    search_value = request.GET.get("search-inp", "")
    if search_value:
        products = Product.objects.filter(
            Q(name__icontains=search_value) | Q(category__cat_name__startswith=search_value)
        )
        selected_cat = f"results for '{search_value}'"
    else:
        products = Product.objects.all()  # get all products from db
        selected_cat = "all"
    
    context = {
                "products": products, 
                "categories": categories,
                "selected_cat": selected_cat, 
               }
    return render(request, "products/product_list.html", context)

def product_details(request, prod_id):
    categories = Category.objects.all()  # get all categories from db
    product = Product.objects.get(id=prod_id)  # get the selected product data from db
    extra_imgs = product.get_images()
    img_num = extra_imgs.count() if extra_imgs else 0
    img_range = range(1, img_num+1)
    stocks = Stock.objects.filter(product=product)
    
    ###########################################
    context = {
                "product": product, 
                "categories": categories,
                "product_imgs" : extra_imgs,
                "img_num" : img_num,
                "img_range" : img_range,
               }
    return render(request, "products/product_details.html", context)