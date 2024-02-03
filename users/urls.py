from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path("seller/", get_seller, name='get-seller'),
    path("seller/add/", add_seller, name='add-seller'),
    path("seller/edit/", edit_seller, name='edit-seller'),
    path("seller/login/", login_seller, name='login-seller'),
    
    path("buyer/", get_buyer, name='get-buyer'),
    path("buyer/add/", add_buyer, name='add-buyer'),
    path("buyer/edit/", edit_buyer, name='edit-buyer'),
    path("buyer/login/", login_buyer, name='login-buyer')
]