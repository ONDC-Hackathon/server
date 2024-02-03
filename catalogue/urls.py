from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path("get_products/", get_products, name="get-products"),
    path("get_product/<int:pk>/", get_product, name="get-products"),
    path("add_product_details/", add_product_details, name="add-product-details"),
    path("edit_product_details/", edit_product_details, name="edit-product-details"),
    path("delete_product/", delete_product, name="delete-product"),
    path("add_product_image/", add_product_image, name="add-product-image"),
    path("delete_product_image/", delete_product_image, name="delete-product-image"),
    path("add_product_attributes/", add_product_attributes, name="add-product-attributes"),
    path("edit_product_attributes/", edit_product_attributes, name="edit-product-attributes"),
    path("delete_product_attributes/", delete_product_attributes, name="delete-product-attributes"),
    path("get_categories/", get_categories, name="get-categories"),
    path("get_sub_categories/<int:pk>/", get_sub_categories, name="get-sub-categories"),
    path("get_variants/<int:pk>/", get_variants, name="get-variants"),
    path("get_attributes/", get_attributes, name="get-attributes"),
]