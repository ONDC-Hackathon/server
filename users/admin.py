from django.contrib import admin
from .models.sellers import *
from .models.buyers import *

# Register your models here.
admin.site.register(Seller)
admin.site.register(Buyer)
