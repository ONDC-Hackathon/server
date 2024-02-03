from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path("seller/register/", register_seller, name='register-seller'),
    path("buyer/register/", register_buyer, name='register-buyer'),
    path("seller/login/", login_seller, name='login-seller'),
    path("buyer/login/", login_buyer, name='login-buyer')
]