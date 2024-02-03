from .base import BaseModel
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Image(BaseModel):
    file = models.FileField(upload_to="images/")
    alternate_text = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.alternate_text