from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/<str:cat_name>/", views.product_list, name="products"),
]