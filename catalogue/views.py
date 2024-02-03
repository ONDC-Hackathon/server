from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from users.serializers import *
from middleware.auth import Authentication
from middleware.permissions import SellerPermission
from copy import deepcopy
from .serializers import *

@api_view(['POST'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def add_product_details(request):
    try:
        data = deepcopy(request.data)
        data["seller"] = Seller.objects.get(user=request.user.id).id

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product Added Successfully", "product": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    

@api_view(['POST'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def add_product_image(request):
    try:
        product = Product.objects.filter(id=request.data['product_id']).first()
        if product is None:
            return Response({"error": "Product not found"}, status=400)
        
        seller = Seller.objects.get(user=request.user.id)
        if product.seller.id != seller.id:
            return Response({"error": "Not Allowed"}, status=403)

        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Image uploaded successfully", "image": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)