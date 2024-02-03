from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path("product/", get_products, name="get-products"),
    path("product/<int:pk>/", get_product, name="get-product"),
    path("product/add/", add_product, name="add-product"),
    path("product/edit/", edit_product, name="edit-product"),
    path("product/delete/", delete_product, name="delete-product"),

    path("product_image/add/", add_product_image, name="add-product-image"),
    path("product_image/delete/", delete_product_image, name="delete-product-image"),

    path("product_attribute/add/", add_product_attributes, name="add-product-attributes"),
    path("product_attribute/edit/", edit_product_attributes, name="edit-product-attributes"),
    path("product_attribute/delete/", delete_product_attributes, name="delete-product-attributes"),
    
    path("category/", get_categories, name="get-categories"),
    path("sub_category/<int:pk>/", get_sub_categories, name="get-sub-categories"),
    path("variant/<int:pk>/", get_variants, name="get-variants"),
    path("attribute/", get_attributes, name="get-attributes"),
]