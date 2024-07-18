from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/<str:cat_name>/", views.product_list, name="products"),
    path("products/search", views.product_search, name="search"),
    path("product/<slug:slug>/", views.product_details, name="product"),
    path("bag", views.bag_details, name="bag"),
    path("add_to_bag/<int:product_id>", views.add_to_bag, name="add_item"),
    path("remove_from_bag/<int:product_id>", views.remove_from_bag, name="remove_item"),
    path("update_bag/<int:product_id>", views.update_bag, name="update_bag"),
]