from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/<str:cat_name>/", views.product_list, name="products"),
    path("products/search", views.product_search, name="search"),
    path("product/<slug:slug>/", views.product_details, name="product"),
    path("bag", views.bag, name="bag"),
]