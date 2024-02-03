from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from users.serializers import *
from middleware.auth import Authentication
from middleware.permissions import SellerPermission
from copy import deepcopy
from .serializers import *
from rest_framework import exceptions


# Product APIs

def check_product_ownership(request):
    product = Product.objects.filter(id=request.data['product_id']).first()
    if product is None:
        raise exceptions.NotFound("Product not found")
    
    seller = Seller.objects.get(user=request.user.id)
    if product.seller.id != seller.id:
        raise exceptions.PermissionDenied("Not Allowed")
    
    return product, seller

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
        product, seller = check_product_ownership(request)

        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Image uploaded successfully", "image": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    

@api_view(['POST'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def add_product_attributes(request):
    try:
        product, seller = check_product_ownership(request)
    
        data = deepcopy(request.data)
        del data["product_id"]
        attributes = [ {"attribute": attr, "value": data[attr], "product": product.id} for attr in data]

        serializer = ProductAttributeSerializer(data=attributes, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product attributes were added successfully", "attributes": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
        
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
@authentication_classes([Authentication])
def get_categories(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"message": "Categories fetched successfully", "categories": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    

@api_view(['GET'])
@authentication_classes([Authentication])
def get_sub_categories(request, pk):
    try:
        category = Category.objects.get(id=pk)
        sub_categories = SubCategory.objects.filter(category=category)
        serializer = SubCategorySerializer(sub_categories, many=True)
        return Response({"message": "Sub-Categories fetched successfully", "sub_categories": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
@authentication_classes([Authentication])
def get_variants(request, pk):
    try:
        sub_category = SubCategory.objects.get(id=pk)
        variants = Variant.objects.filter(sub_category=sub_category)
        serializer = VariantSerializer(variants, many=True)
        return Response({"message": "Variants fetched successfully", "variants": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
@authentication_classes([Authentication])
def get_attributes(request):
    try:
        attributes = Attribute.objects.all()
        if "category" in request.GET:
            attributes = attributes.filter(category=request.GET["category"])
        if "sub_category" in request.GET:
            attributes = attributes.filter(sub_category=request.GET["sub_category"])
        if "variant" in request.GET:
            attributes = attributes.filter(variant=request.GET["variant"])

        serializer = AttributeSerializer(attributes, many=True)
        return Response({"message": "Variants fetched successfully", "attributes": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
