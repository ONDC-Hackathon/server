from .base import BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .products import *
from .attributes import *
from .rules import *

class ProductAttribute(BaseModel):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, related_name='attributes', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    # weight = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)

    def __str__(self):
        return self.product.title + " - " + self.attribute.title

class ProductLog(BaseModel):
    product = models.ForeignKey(Product, related_name='attribute_logs', on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, related_name='attribute_logs', on_delete=models.CASCADE,null=True, blank=True)
    image=models.ForeignKey(Image, related_name='attribute_logs', on_delete=models.CASCADE,null=True, blank=True)
    is_okay = models.BooleanField(default=False)
    description=models.TextField(null=True, blank=True)
    gcp_data=models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.product.title