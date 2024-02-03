from rest_framework import serializers
from django.contrib.auth.models import User
from .models.sellers import *
from .models.buyers import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buyer
        fields = '__all__'