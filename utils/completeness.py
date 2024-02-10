import numpy as np
from PIL import Image, ImageFilter
from catalogue.models.attributes import Attribute
from catalogue.models.products import Product
from catalogue.models.relations import ProductAttribute


ATTRIBUTE_WEIGHT = 0.4
IMAGE_WEIGHT = 0.3
IMAGE_QUALITY_WEIGHT = 0.3


def calculate_completeness_score(product):
    try:
        attributes = Attribute.objects.filter(category=product.category)
        attributes.union(attributes, Attribute.objects.filter(
            sub_category=product.sub_category))
        attributes.union(Attribute.objects.filter(variant=product.variant))
        product_attributes = ProductAttribute.objects.filter(product=product)
        attribute_score = product_attributes.count()/attributes.count()
        image_score = product.images.all().count()/6
        image_quality_score = calculate_image_quality_score(product)
        return (ATTRIBUTE_WEIGHT*attribute_score + IMAGE_WEIGHT*image_score+IMAGE_QUALITY_WEIGHT*image_quality_score)/(attribute_score + image_score+image_quality_score)
    except Exception as e:
        print(e)
        return 0


def calculate_image_quality_score(product):
    quality_scores = []

    for image_instance in product.images.all():  # Assuming this method returns a list of image paths
        try:
            img = Image.open(image_instance.file)

            # High quality criteria

            # 1. Resolution: Higher resolution contributes to a higher score
            # Normalized against 720p resolution
            resolution_score = min((img.width * img.height) / 1920*1080, 1)
            # print(f"Resolution score: {resolution_score}")

            # 2. Sharpness: Use edge enhancement as a proxy for sharpness
            sharp_img = img.filter(ImageFilter.EDGE_ENHANCE)
            # Normalizing against max pixel value
            sharpness_score = np.mean(np.array(sharp_img)) / 255
            # print(f"Sharpness score: {sharpness_score}")

            # 3. Noise: Simple variance calculation as a proxy for noise (lower variance might indicate less noise)
            # This is a simplistic approach and may not accurately reflect true image noise
            # Convert to grayscale for simplicity
            img_array = np.array(img.convert('L'))
            variance = np.var(img_array)
            # Normalizing variance; this threshold is arbitrary
            noise_score = 1 - min(variance / 5000, 1)
            # print(f"Noise score: {noise_score}")

            # Combine scores: This is a simple average; you may weigh factors differently
            combined_score = (resolution_score +
                              sharpness_score + noise_score) / 3
            # print(f"Combined score: {combined_score}")
            quality_scores.append(combined_score)
        except Exception as e:
            print(f"Error processing image {image_instance}: {e}")
            quality_scores.append(0)

    if quality_scores:
        return sum(quality_scores) / len(quality_scores)
    else:
        return 0
