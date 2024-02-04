from .base import BaseModel
from django.db import models
from users.models.sellers import *
from .categories import Category, SubCategory, Variant

class Rule(BaseModel):
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='rules', on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, related_name='rules', on_delete=models.SET_NULL, null=True, blank=True)
    variant = models.ForeignKey(Variant, related_name='rules', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.description