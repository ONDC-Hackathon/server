from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path("add_product_details/", add_product_details, name="add-product-details"),
    path("add_product_image/", add_product_image, name="add-product-image"),
    path("add_product_attributes/", add_product_attributes, name="add-product-attributes"),
    path("get_categories/", get_categories, name="get-categories"),
    path("get_sub_categories/<int:pk>/", get_sub_categories, name="get-sub-categories"),
    path("get_variants/<int:pk>/", get_variants, name="get-variants"),
    path("get_attributes/", get_attributes, name="get-attributes"),
]