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

@api_view(['GET'])
@authentication_classes([Authentication])
def get_products(request):
    try:
        products = Product.objects.all()
        if "category" in request.GET:
            products = products.filter(category=Category.objects.get(id=request.GET["category"]))
        
        if "sub_category" in request.GET:
            products = products.filter(sub_category=SubCategory.objects.get(id=request.GET["sub_category"]))

        if "variant" in request.GET:
            products = products.filter(variant=Variant.objects.get(id=request.GET["variant"]))
        
        serializer = ProductSerializer(products, many=True)
        return Response({"message": "Products fetched successfully", "data": serializer.data}, status=200)
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
@authentication_classes([Authentication])
def get_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        attributes = ProductAttribute.objects.filter(product=product)

        basics = ProductSerializer(product)
        details = ProductAttributeSerializer(attributes, many=True)

        return Response({"message": "Products fetched successfully", "data": {"basics": basics.data, "details": details.data}}, status=200)
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)


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
            return Response({"message": "Product Added Successfully", "data": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['PUT'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def edit_product_details(request):
    try:
        product, seller = check_product_ownership(request)

        data = deepcopy(request.data)
        del data['product_id']
        data["seller"] = seller.id

        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product details updated successfully", "data": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
 
@api_view(['DELETE'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def delete_product(request):
    try:
        product, seller = check_product_ownership(request)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=200)
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
            return Response({"message":"Image uploaded successfully", "data": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['DELETE'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def delete_product_image(request):
    try:
        product, seller = check_product_ownership(request)
        image = Image.objects.get(id=request.data["image_id"])
        if image not in product.images.all():
            return Response({"error":"Not Allowed"}, status=403)
        image.delete()
        return Response({"message":"Image deleted successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def add_product_attributes(request):
    try:
        product, seller = check_product_ownership(request)

        attributes = [ {"attribute": attr, "value": request.data["attributes"][attr], "product": product.id} for attr in request.data["attributes"]]

        serializer = ProductAttributeSerializer(data=attributes, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product attributes were added successfully", "data": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
        
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['PUT'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def edit_product_attributes(request):
    try:
        product, seller = check_product_ownership(request)

        attributes = [ProductAttribute.objects.get(id=attr) for attr in request.data['attributes']]

        for attribute in attributes:
            if attribute.product != product:
                return Response({"error": "Not Allowed"}, status=400)

        for attribute in attributes:
            attribute.value = request.data['attributes'][str(attribute.id)]
            attribute.save()

        return Response({"message": "Product attributes updated successfully"}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['DELETE'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def delete_product_attributes(request):
    try:
        product, seller = check_product_ownership(request)

        attributes = [ProductAttribute.objects.get(id=attr) for attr in request.data["attributes"]]

        for attribute in attributes:
            if attribute.product != product:
                return Response({"error": "Not Allowed"}, status=400)

        for attribute in attributes:
            attribute.delete()

        return Response({"message": "Product attributes deleted successfully"}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
@authentication_classes([Authentication])
def get_categories(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"message": "Categories fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    

@api_view(['GET'])
@authentication_classes([Authentication])
def get_sub_categories(request, pk):
    try:
        category = Category.objects.get(id=pk)
        sub_categories = SubCategory.objects.filter(category=category)
        serializer = SubCategorySerializer(sub_categories, many=True)
        return Response({"message": "Sub-Categories fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
@api_view(['GET'])
@authentication_classes([Authentication])
def get_variants(request, pk):
    try:
        sub_category = SubCategory.objects.get(id=pk)
        variants = Variant.objects.filter(sub_category=sub_category)
        serializer = VariantSerializer(variants, many=True)
        return Response({"message": "Variants fetched successfully", "data": serializer.data}, status=200)
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
        return Response({"message": "Variants fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
