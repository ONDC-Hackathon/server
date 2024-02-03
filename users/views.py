from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import *
from copy import deepcopy
import datetime
import jwt
from django.contrib.auth import authenticate

@api_view(['POST'])
def register_seller(request):
    try:
        user = UserSerializer(data=request.data["user"])
        if user.is_valid():
            user = user.save()
        else:
            return Response({"error": user.errors}, status=400)
        
        data = deepcopy(request.data["seller"])
        data["user"] = user.id

        seller = SellerSerializer(data=data)
        if seller.is_valid():
            seller.save()
        else:
            User.objects.get(id=user.id).delete()
            return Response({"error": seller.errors}, status=400)
    
        return Response({"message": "Account Created Successfully"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['POST'])
def register_buyer(request):
    try:
        user = UserSerializer(data=request.data["user"])
        if user.is_valid():
            user = user.save()
        else:
            return Response({"error": user.errors}, status=400)
        
        data = deepcopy(request.data["buyer"])
        data["user"] = user.id

        buyer = BuyerSerializer(data=data)
        if buyer.is_valid():
            buyer.save()
        else:
            User.objects.get(id=user.id).delete()
            return Response({"error": buyer.errors}, status=400)
    
        return Response({"message": "Account Created Successfully"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    

@api_view(['POST'])
def login_seller(request):
    try:
        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error":"Incorrect credentials"}, status=401)
        
        seller = Seller.objects.filter(user=user).first()

        if seller is None:
            return Response({"error":"No seller exists with these credentials"}, status=401)
        
        payload = {
            "id": user.id,
            "type": "seller",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=129600),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'SECRET', algorithm='HS256')

        data = dict()
        data["user"] = UserSerializer(user).data
        data["seller"] = SellerSerializer(seller).data

        return Response({"message": "Seller Login Sucessful", "token": token, "data": data}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['POST'])
def login_buyer(request):
    try:
        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error":"Incorrect credentials"}, status=401)
        
        buyer = Buyer.objects.filter(user=user).first()

        if buyer is None:
            return Response({"error":"No buyer exists with these credentials"}, status=401)
        
        payload = {
            "id": user.id,
            "type": "buyer",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=129600),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'SECRET', algorithm='HS256')

        data = dict()
        data["user"] = UserSerializer(user).data
        data["buyer"] = BuyerSerializer(buyer).data

        return Response({"message": "Buyer Login Sucessful", "token": token, "data": data}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)