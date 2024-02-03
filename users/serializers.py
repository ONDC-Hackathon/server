from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models.sellers import *
from .models.buyers import *

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buyer
        fields = '__all__'