from .base import BaseModel
from django.contrib.auth.models import User
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Buyer(BaseModel):
    user = models.OneToOneField(User, related_name="buyer", on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid phone number.",
                code="invalid_phone_number",
            ),
        ])
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    address_line_3 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=7,  validators=[
            RegexValidator(
                regex=r'^[1-9]{1}[0-9]{2}\s{0,1}[0-9]{3}$',
                message="Enter a valid pincode.",
                code="invalid_pincode",
            ),
        ])
    additional_contact = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username