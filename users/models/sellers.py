from .base import BaseModel
from django.contrib.auth.models import User
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Seller(BaseModel):
    user = models.OneToOneField(User, related_name="seller", on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Enter a valid phone number.",
                code="invalid_phone_number",
            ),
        ])
    aadhaar = models.CharField(max_length=14, validators=[
            RegexValidator(
                regex=r'^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$',
                message="Enter a valid aadhaar number.",
                code="invalid_aadhaar_number",
            ),
        ])
    gstin = models.CharField(max_length=15,  validators=[
            RegexValidator(
                regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$',
                message="Enter a valid GSTIN.",
                code="invalid_gstin",
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



    
