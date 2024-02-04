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

    path("rule/", get_rules, name="get-rules"),
    path("rule/<int:pk>/", get_rule, name="get-rule"),

    path("product_rule/<int:product_id>/", get_product_rules, name="get-product-rules"),
    path("product_rule/<int:product_id>/<int:pk>/", get_product_rule, name="get-product-rule"),
    path("product_rule/add/", add_product_rules, name="add-product-rules"),
    path("product_rule/delete/", delete_product_rules, name="delete-product-rules"),
    
    path("category/", get_categories, name="get-categories"),
    path("sub_category/<int:pk>/", get_sub_categories, name="get-sub-categories"),
    path("variant/<int:pk>/", get_variants, name="get-variants"),
    path("attribute/", get_attributes, name="get-attributes"),
]