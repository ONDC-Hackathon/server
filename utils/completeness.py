from catalogue.models.attributes import Attribute
from catalogue.models.products import Product
from catalogue.models.relations import ProductAttribute


ATTRIBUTE_WEIGHT = 0.8
IMAGE_WEIGHT = 0.2

def calculate_completeness_score(product):
    attributes = Attribute.objects.filter(category=product.category)
    attributes.union(attributes, Attribute.objects.filter(sub_category=product.sub_category))
    attributes.union(Attribute.objects.filter(variant=product.variant))
    product_attributes = ProductAttribute.objects.filter(product=product)
    attribute_score = product_attributes.count()/attributes.count()
    image_score = product.images.all().count()/6
    return (ATTRIBUTE_WEIGHT*attribute_score + IMAGE_WEIGHT*image_score)/(attribute_score + image_score)