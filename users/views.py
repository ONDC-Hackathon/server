from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from users.serializers import *
from copy import deepcopy
import datetime
import jwt
from django.contrib.auth import authenticate
from middleware.auth import *
from middleware.permissions import *
from rest_framework.views import APIView

# class SellerView(APIView):
#     authentication_classes = [Authentication]
#     permission_classes = [SellerPermission]
    

@api_view(['GET'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def get_seller(request):
    try:
        data = dict()
        data["user"] = UserSerializer(request.user).data
        data["seller"] = SellerSerializer(Seller.objects.get(user=request.user.id)).data
        return Response({"message": "Seller details fetched successfully", "data": data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def add_seller(request):
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

@api_view(['PUT'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def edit_seller(request):
    try:  
        data = dict()
        if "user" in request.data:
            serializer = UserSerializer(request.user, data=request.data["user"], partial=True)
            if serializer.is_valid():
                serializer.save()
                data["user"] = serializer.data
            else:
                return Response({"error": serializer.errors}, status=400)
        
        if "seller" in request.data:
            seller = Seller.objects.get(user=request.user.id)
            serializer = SellerSerializer(seller, data=request.data["seller"], partial=True)
            if serializer.is_valid():
                serializer.save()
                data["seller"] = serializer.data
            else:
                return Response({"error": serializer.errors}, status=400)
        return Response({"message": "Seller details updated sucessfuly", "data": data}, status=200)
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

@api_view(['GET'])
@authentication_classes([Authentication])
@permission_classes([BuyerPermission])
def get_buyer(request):
    try:
        data = dict()
        data["user"] = UserSerializer(request.user).data
        data["buyer"] = BuyerSerializer(Buyer.objects.get(user=request.user.id)).data
        return Response({"message": "Buyer details fetched successfully", "data": data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def add_buyer(request):
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
    
@api_view(['PUT'])
@authentication_classes([Authentication])
@permission_classes([BuyerPermission])
def edit_buyer(request):
    try:  
        data = dict()
        if "user" in request.data:
            serializer = UserSerializer(request.user, data=request.data["user"], partial=True)
            if serializer.is_valid():
                serializer.save()
                data["user"] = serializer.data
            else:
                return Response({"error": serializer.errors}, status=400)
        
        if "buyer" in request.data:
            buyer = Buyer.objects.get(user=request.user.id)
            serializer = BuyerSerializer(buyer, data=request.data["buyer"], partial=True)
            if serializer.is_valid():
                serializer.save()
                data["buyer"] = serializer.data
            else:
                return Response({"error": serializer.errors}, status=400)
        return Response({"message": "Buyer details updated sucessfuly", "data": data}, status=200)
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
    


