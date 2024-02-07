from .base import BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from users.models.sellers import *
from .categories import Category, SubCategory, Variant

class Attribute(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, related_name="attribute", blank=True)
    sub_category = models.ManyToManyField(SubCategory, related_name="attribute", blank=True)
    variant = models.ManyToManyField(Variant, related_name="attribute", blank=True)

    def __str__(self):
        return self.title