from .base import BaseModel
from django.db import models
from users.models.sellers import *
from .categories import Category, SubCategory, Variant
import os

from django.core.files.storage import FileSystemStorage


class RuleFileStorage(FileSystemStorage):
    """
    Custom storage class to store uploaded files for the "Rule" model in a "rules" folder.
    """

    base_url = ''  # Set base URL if needed for URLs or media path construction
    location = 'rules'  # Folder name within the root project directory

    def get_available_name(self, name, max_length=None):
        """
        Customizes file name generation to avoid conflicts.
        """
        # Implement your desired naming logic here (e.g., using timestamps)
        return super().get_available_name(name, max_length)

    def path(self, name):
        """
        Overrides the path method to build the custom file path.
        """
        return os.path.join(self.location, name)

class Rule(BaseModel):
    description = models.TextField()
    file = models.FileField(upload_to='', storage=RuleFileStorage(), null=True, blank=True)
    weight = models.DecimalField(max_digits=20, decimal_places=5)
    category = models.ManyToManyField(Category, related_name='rules', blank=True)
    sub_category = models.ManyToManyField(SubCategory, related_name='rules', blank=True)
    variant = models.ManyToManyField(Variant, related_name='rules', blank=True)

    def __str__(self):
        return self.description