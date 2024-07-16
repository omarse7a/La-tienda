from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.cache import cache_page
from .models import Product, Category, Stock

# Create your views here.
def index(request):
    return render(request, "shopping/bag.html")


# Product related views
@cache_page(60 * 15)    # Cache for 15 minutes
def product_list(request, cat_name):
    categories = Category.objects.all() # get all categories from db

    # Filter by selected category
    if cat_name == "all":
        products = Product.objects.filter(active=True)  # get all products from db
    else:
        category = Category.objects.get(cat_name=cat_name)
        products = category.get_cat_products()  # get all active products by this category

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
        products = Product.objects.filter(active=True)  # get all active products from db
        selected_cat = "all"
    
    context = {
                "products": products, 
                "categories": categories,
                "selected_cat": selected_cat, 
               }
    return render(request, "products/product_list.html", context)

@cache_page(60 * 15)    # Cache for 15 minutes
def product_details(request, slug):
    categories = Category.objects.all()  # get all categories from db
    product = Product.objects.get(slug=slug)  # get the selected product data from db
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
                "stocks" : stocks,
               }
    return render(request, "products/product_details.html", context)