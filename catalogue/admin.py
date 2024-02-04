from django.contrib import admin
from .models.categories import *
from .models.products import *
from .models.attributes import *
from .models.images import *
from .models.relations import *
from .models.rules import *

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Variant)
admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(Image)
admin.site.register(ProductAttribute)
admin.site.register(Rule)
admin.site.register(ProductRule)
