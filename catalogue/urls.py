from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path("add_product_details/", add_product_details, name="add-product-details"),
    path("add_product_images/", add_product_images, name="add-product-images"),
]