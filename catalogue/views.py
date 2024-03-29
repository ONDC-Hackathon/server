from catalogue.tasks import *
from copy import deepcopy

from rest_framework import exceptions
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes, parser_classes)
from rest_framework.response import Response

from middleware.auth import Authentication
from middleware.permissions import BuyerPermission, SellerPermission
from users.serializers import *

from .serializers import *
from rest_framework import exceptions
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser

#################################################################################################

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
        products = Product.objects.filter(seller=Seller.objects.get(user=request.user.id))
        if "category" in request.GET:
            products = products.filter(
                category=Category.objects.get(id=request.GET["category"]))

        if "sub_category" in request.GET:
            products = products.filter(
                sub_category=SubCategory.objects.get(id=request.GET["sub_category"]))

        if "variant" in request.GET:
            products = products.filter(
                variant=Variant.objects.get(id=request.GET["variant"]))

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
def add_product(request):
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
def edit_product(request):
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
        for image in product.images.all():
            image.delete()
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


#################################################################################################

# Image APIs

@api_view(['POST'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
@parser_classes([FormParser, MultiPartParser])
def add_product_image(request):
    try:
        data = deepcopy(request.data.dict())
        images_array = []
        for key in data.keys():
            if key.startswith('images'):
                image_index = int(key.split('[')[1].split(']')[0])
                attribute = key.split('[')[-1].split(']')[0]
                if len(images_array) > image_index:
                    images_array[image_index][attribute] = data[key]
                else:
                    images_array.append({attribute: data[key]})

        product, seller = check_product_ownership(request)
        serializer = ImageSerializer(data=images_array, many=True)

        if serializer.is_valid():
            images = serializer.save()
            product.images.add(*images)
            product.save()
            return Response({"message": "Image uploaded successfully", "data": serializer.data}, status=200)
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
            return Response({"error": "Not Allowed"}, status=403)
        image.delete()
        return Response({"message": "Image deleted successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


#################################################################################################

# Attribute APIs

@api_view(['GET'])
@authentication_classes([Authentication])
def get_attributes(request):
    try:
        attributes = Attribute.objects.filter(category=request.GET["category"])
        if "sub_category" in request.GET:
            attributes = attributes.union(attributes, Attribute.objects.filter(
                sub_category=request.GET["sub_category"]))
        if "variant" in request.GET:
            attributes = attributes.union(attributes, Attribute.objects.filter(
                variant=int(request.GET["variant"])))

        serializer = AttributeSerializer(attributes, many=True)
        return Response({"message": "Attributes fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def add_product_attributes(request):
    try:
        product, seller = check_product_ownership(request)

        attributes = [{"attribute": attr, "value": request.data["attributes"]
                       [attr], "product": product.id} for attr in request.data["attributes"]]

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

        attributes = [ProductAttribute.objects.get(
            id=attr) for attr in request.data['attributes']]

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

        attributes = [ProductAttribute.objects.get(
            id=attr) for attr in request.data["attributes"]]

        for attribute in attributes:
            if attribute.product != product:
                return Response({"error": "Not Allowed"}, status=400)

        for attribute in attributes:
            attribute.delete()

        return Response({"message": "Product attributes deleted successfully"}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


#################################################################################################

# Rules APIs


@api_view(['GET'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def get_rules(request):
    try:
        rules = Rule.objects.all()
        if "category" in request.GET:
            rules = Rule.objects.filter(category=request.GET["category"])
        if "sub_category" in request.GET:
            rules = Rule.objects.filter(
                sub_category=request.GET["sub_category"])
        if "variant" in request.GET:
            rules = Rule.objects.filter(variant=request.GET["variant"])
        serializer = RuleSerializer(rules, many=True)
        return Response({"message": "Rules fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([Authentication])
@permission_classes([SellerPermission])
def get_rule(request, pk):
    try:
        rule = Rule.objects.get(id=pk)
        serializer = RuleSerializer(rule)
        return Response({"message": "Rule fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


#################################################################################################

# Review APIs

@api_view(['GET'])
@authentication_classes([Authentication])
def get_reviews(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response({"message": "Reviews fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([Authentication])
def get_review(request, product_id, pk):
    try:
        product = Product.objects.get(id=product_id)
        reviews = Review.objects.filter(product=product).get(id=pk)
        serializer = ReviewSerializer(reviews)
        return Response({"message": "Reviews fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
@authentication_classes([Authentication])
@permission_classes([BuyerPermission])
def add_review(request):
    try:
        data = deepcopy(request.data)
        data["buyer"] = request.user.buyer.id
        data["product"] = request.data["product_id"]
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Review added successfully", "data": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['PUT'])
@authentication_classes([Authentication])
@permission_classes([BuyerPermission])
def edit_review(request):
    try:
        review = Review.objects.get(id=request.data["review_id"])
        if review.buyer.user != request.user:
            return Response({"error": "Not Allowed"}, status=403)
        data = deepcopy(request.data)
        data["product"] = review.product.id
        data["buyer"] = request.user.buyer.id
        serializer = ReviewSerializer(review, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Review added successfully", "data": serializer.data}, status=200)
        else:
            return Response({"error": serializer.errors}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['DELETE'])
@authentication_classes([Authentication])
@permission_classes([BuyerPermission])
def delete_review(request):
    try:
        review = Review.objects.get(id=request.data["review_id"])
        if review.buyer.user != request.user:
            return Response({"error": "Not Allowed"}, status=403)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


#################################################################################################

# Category APIs


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
def get_sub_categories(request):
    try:
        sub_categories = SubCategory.objects.all()
        if "category" in request.GET:
            sub_categories = sub_categories.filter(
                category=int(request.GET["category"]))
        serializer = SubCategorySerializer(sub_categories, many=True)
        return Response({"message": "Sub-Categories fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

#################################################################################################

# Variant APIs


@api_view(['GET'])
@authentication_classes([Authentication])
def get_variants(request):
    try:
        variants = Variant.objects.all()
        if "sub_category" in request.GET:
            variants = variants.filter(
                sub_category=int(request.GET["sub_category"]))
        serializer = VariantSerializer(variants, many=True)
        return Response({"message": "Variants fetched successfully", "data": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

##################################################################################################


# Evaluate Score


@api_view(['GET'])
@authentication_classes([Authentication])
# @permission_classes([SellerPermission])
def evaluate_score(request, pk):
    try:
        product = Product.objects.filter(id=pk).first()
        if product is None:
            raise exceptions.NotFound("Product not found")
        if product.scoring_status == 'Processing':
            return Response({"message": "Product is under review"}, status=200)
        # seller = Seller.objects.get(user=request.user.id)
        # if product.seller.id != seller.id:
        #     raise exceptions.PermissionDenied("Not Allowed")
        product.scoring_status = 'Processing'
        product.save()
        start_background_task(pk)
        return Response({"message": "Score is Being Evaluated"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
@authentication_classes([Authentication])
# @permission_classes([SellerPermission])
def check_score(request, pk):
    try:
        product = Product.objects.get(id=pk)
        if not product:
            return Response({"error": "Product not found"}, status=404)
        logs = product.attribute_logs.filter(is_okay=False)
        serializer = ProductLogSerializer(logs, many=True)
        return Response({"message": "Logs Fetched Sucessfully", "logs": serializer.data}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
