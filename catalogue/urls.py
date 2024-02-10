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
    
    path("evaluate_score/<int:pk>/", evaluate_score, name="evaluate-score"),
    path("check_score/<int:pk>/", check_score, name="check-score"),

    path("rule/", get_rules, name="get-rules"),
    path("rule/<int:pk>/", get_rule, name="get-rule"),

    path("review/<int:product_id>/", get_reviews, name="get-reviews"),
    path("review/<int:product_id>/<int:pk>/", get_review, name="get-review"),
    path("review/add/", add_review, name="add-review"),
    path("review/edit/", edit_review, name="edit-review"),
    path("review/delete/", delete_review, name="delete-review"),
    
    path("category/", get_categories, name="get-categories"),
    path("sub_category/<int:pk>/", get_sub_categories, name="get-sub-categories"),
    path("variant/<int:pk>/", get_variants, name="get-variants"),
    path("attribute/", get_attributes, name="get-attributes"),
]