from .base import BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from users.models.sellers import *
from .categories import Category, SubCategory, Variant
from .images import Image

STATUS_CHOICES = (
    ('Available', 'Available'),
    ('Unavailable', 'Unavailable'),
)

SCORING_STATUS_CHOICES = (
    ('Uninitialized', 'Uninitialized'),
    ('Processing', 'Processing'),
    ('Completed', 'Completed'),
    ('Published', 'Published')
)

class Product(BaseModel):
    seller = models.ForeignKey(Seller, related_name="product", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Available')
    available_stock = models.BigIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=5)
    tax = models.DecimalField(max_digits=20, decimal_places=5)
    discount = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, related_name="product", on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, related_name="product", on_delete=models.SET_NULL, null=True, blank=True)
    compliance_score = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    completeness_score = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    correctness_score = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    catalogue_score = models.DecimalField(max_digits=20, decimal_places=5, null=True, blank=True)
    scoring_status = models.CharField(max_length=20, choices=SCORING_STATUS_CHOICES, default='Uninitialized')
    images = models.ManyToManyField(Image, related_name="product", blank=True)

    def __str__(self):
        return self.title
