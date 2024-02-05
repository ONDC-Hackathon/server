from .base import BaseModel
from django.contrib.auth.models import User
from django.db import models
from .products import *
from users.models.buyers import *
from django.core.validators import MaxValueValidator, MinValueValidator 

class Review(BaseModel):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, related_name='reviews', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.product.title + " reviewed by " + self.buyer.user.username