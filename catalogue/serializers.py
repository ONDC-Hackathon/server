from rest_framework import serializers
from .models.categories import *
from .models.attributes import *
from .models.images import *
from .models.products import *

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'