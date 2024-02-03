from .base import BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .products import *
from .attributes import *

class ProductAttribute(BaseModel):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, related_name='attributes', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.product.title + " - " + self.attribute.title