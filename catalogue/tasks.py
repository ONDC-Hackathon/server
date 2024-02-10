import threading
import json
from catalogue.models.products import *
from utils.completeness import calculate_completeness_score
from utils.compliance import calculate_compliance_score
from utils.correctness import calculate_correctness_score
from utils.imageVerification import extract_text_from_image_file
from utils.proFanityCheck import analyze_and_flag_negative_sentiment
from catalogue.serializers import ProductLogSerializer


COMPLETENESS_WEIGHT = 0.3
COMPLIANCE_WEIGHT = 0.2
CORRECTNESS_WEIGHT = 0.5


def long_running_task(pk):
    print("Task started")
    product = Product.objects.prefetch_related(
        'attributes', 'images').get(pk=pk)

    # check for previous logs and delete all of them if any one is_okay is false
    logs = product.attribute_logs.all()
    all_product_okay = all(
        [log.is_okay for log in logs])
    log_count = logs.count()

    if not all_product_okay or log_count == 0:
        logs.delete()
        check_on_quality_of_attributes(product)
    completeness_score = 0
    compliance_score = 0
    correctness_score = 0
    catalouge_score = 0
    try:
        completeness_score = calculate_completeness_score(product)
        compliance_score = calculate_compliance_score(product)
        correctness_score = calculate_correctness_score(product)
        catalouge_score = (completeness_score * COMPLETENESS_WEIGHT + compliance_score *
                           COMPLIANCE_WEIGHT + correctness_score * CORRECTNESS_WEIGHT)
    except Exception as e:
        print(e)
        print("Error calculating scores")
    product.completeness_score = completeness_score
    product.compliance_score = compliance_score
    product.correctness_score = correctness_score
    product.catalogue_score = catalouge_score
    product.scoring_status = "Completed"
    print(f"Completeness score: {completeness_score}")
    print(f"Compliance score: {compliance_score}")
    print(f"Correctness score: {correctness_score}")
    print(f"Catalogue score: {catalouge_score}")
    product.save()

    print("Task completed")


# checking validity of attributes and images whether or not they are vulgar or not
def check_on_quality_of_attributes(product):
    try:
        text_attribute_quality(product.id, product.attributes.all())
        image_attribute_quality(product.id, product.images.all())
    except Exception as e:
        print(e)


def text_attribute_quality(prod_id, attributes):
    for attribute in attributes:
        print("Analyzing attribute:", attribute.value)
        is_okay = not analyze_and_flag_negative_sentiment(attribute.value)
        product_log_data = {
            'product': prod_id,
            'attribute': attribute.id,
            'is_okay': is_okay
        }
        if not is_okay:
            product_log_data['description'] = f"Attribute value "" {attribute.value} "" has quality issues"

        product_log = ProductLogSerializer(data=product_log_data)
        if product_log.is_valid():
            product_log.save()
            # print(product_log.validated_data)


def image_attribute_quality(prod_id, images):
    for image in images:
        print("Analyzing image: ", image.id)
        try:
            analysis_result = extract_text_from_image_file(image)
            safe_search = analysis_result["safe_search_annotation"]
            is_okay = safe_search['adult'] in [1, 2] and safe_search['racy'] in [
                1, 2]  # 1: "Very unlikely", 2: "Unlikely"
            for textInImage in analysis_result['text_annotations']:
                is_okay = is_okay and not analyze_and_flag_negative_sentiment(
                    textInImage['description'])
            product_log_data = {
                'product': prod_id,
                'image': image.id,
                'is_okay': is_okay,
                'gcp_data': json.dumps(analysis_result)
            }
            if not is_okay:
                product_log_data['description'] = f"Image  {image.id}  has quality issues"
            product_log_serializer = ProductLogSerializer(
                data=product_log_data)
            if product_log_serializer.is_valid():
                product_log_serializer.save()
                # print(product_log_serializer.validated_data)
            else:
                print(
                    f"Invalid product log data: {product_log_serializer.errors}")
        except Exception as e:
            # Handle the exception gracefully
            print(f"Error processing image {image.id}: {e}")


# calculate scores in background


def start_background_task(pk):
    thread = threading.Thread(target=long_running_task, args=(pk,))
    thread.start()
