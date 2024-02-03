from .base import BaseModel
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Category(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class SubCategory(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name="sub_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Variant(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, related_name="variant", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

