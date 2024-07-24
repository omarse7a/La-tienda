from django.shortcuts import redirect, render
from django.db.models import Q
from django.views.decorators.cache import cache_page
from .models.product_models import Product, Category, Stock
from .utils import get_bag, get_governorates
from django.contrib import messages
from .forms import ShippingInfoForm

# Landing page view
def index(request):
    return render(request, "home.html")


################ Product related views ################
# @cache_page(60 * 15)    # Cache for 15 minutes
def product_list(request, cat_name):
    categories = Category.objects.all() # get all categories from db

    # Filter by selected category
    if cat_name == "all":
        products = Product.objects.filter(active=True)  # get all products from db
    else:
        category = Category.objects.get(cat_name=cat_name)
        products = category.cat_products  # get all active products by this category

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

# @cache_page(60 * 15)    # Cache for 15 minutes
def product_details(request, slug):
    categories = Category.objects.all()  # get all categories from db
    product = Product.objects.get(slug=slug)  # get the selected product data from db
    extra_imgs = product.images
    img_num = product.image_count
    img_range = range(1, img_num+1)
    stocks = Stock.objects.filter(product=product)
    
    context = {
                "product": product, 
                "categories": categories,
                "product_imgs" : extra_imgs,
                "img_num" : img_num,
                "img_range" : img_range,
                "stocks" : stocks,
               }
    return render(request, "products/product_details.html", context)

################ Bag views ################
def bag_details(request):
    bag = get_bag(request)
    items = bag.bag_items
    return render(request, "shopping/bag.html", {"bag": bag, "bag_items" : items})

def add_to_bag(request, product_id):
    if request.method == "POST":
        bag = get_bag(request)
        product = Product.objects.get(id=product_id)
        size = request.POST.get("size")
        
        bag.add_item(product, size)
    return redirect("bag")

def remove_from_bag(request, product_id):
    if request.method == "POST":
        bag = get_bag(request)
        product = Product.objects.get(id=product_id)
        size = request.POST.get("size")

        bag.remove_item(product, size)
    return redirect("bag")

def update_bag(request, product_id):
    if request.method == "POST":
        bag = get_bag(request)
        product = Product.objects.get(id=product_id)
        size = request.POST.get("size")
        quantity = request.POST.get("quantity")

        bag.update_item(product, size, quantity)
    return redirect("bag")

################ Checkout views ################

def checkout_details(request):
    bag = get_bag(request)
    items = bag.bag_items
    shipping_value = 50
    governorates = get_governorates()
    error_msgs = []

    for item in items:
        try:
            item.adjust_quantity()
        except ValueError as e:
            error_msgs.append(str(e))

    if error_msgs:
        for msg in error_msgs:
            messages.error(request, msg)
        return redirect("bag")
    
    form = ShippingInfoForm()

    context = {"bag": bag, 
               "bag_items" : items,
               "shipping" : shipping_value,
               "governorates" : governorates,
               "form" : form,
               }
    return render(request, "shopping/checkout.html", context)

def confirm_order(request):
    if request.method == "POST":
        bag = get_bag(request)
        items = bag.bag_items
        form = ShippingInfoForm(request.POST)
        if form.is_valid():
            # Save shipping info
            shipping_info = form.save()
            # Adjust quantities and collect errors
            errors = []
            for item in items:
                try:
                    item.adjust_quantity()
                except ValueError as e:
                    errors.append(str(e))

            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect("bag")
            # Confirm the order
            bag.mark_as_ordered(shipping_info)
            # deallocating the stock
            for item in items:
                item.deallocate_stock()

            # Create a new bag for the session
            request.session.create() ###########
            messages.success(request, 'Order confirmed successfully.')

        else:
            messages.error(request, "Please correct the errors in the form.")
    return redirect('checkout')