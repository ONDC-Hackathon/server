from rest_framework import serializers
from .models.categories import *
from .models.attributes import *
from .models.images import *
from .models.products import *
from .models.relations import *

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Variant
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

    compliance_score = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=5)
    completeness_score = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=5)
    correctness_score = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=5)
    catalogue_score = serializers.DecimalField(read_only=True, max_digits=20, decimal_places=5)
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = '__all__'