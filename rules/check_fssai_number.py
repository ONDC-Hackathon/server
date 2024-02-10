import random
import json
import re


def calculate(product):
    gcp_data_raw = product.attribute_logs.all().filter(
        product=product).first().gcp_data
    gcp_data = json.loads(gcp_data_raw)
    gcp_data = gcp_data['text_annotations']
    texts = [text['description'] for text in gcp_data]
    print(texts)
    regex = r"Lic\s*no\.\s*(\d+)"
    for text in texts:
        # re.IGNORECASE makes the search case-insensitive
        match = re.search(regex, text, re.IGNORECASE)
        if match:
            return 1
        else:
            return 0
