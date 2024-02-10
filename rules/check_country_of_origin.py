import random
import json
import re


def calculate(product):
    allData = product.attribute_logs.all().filter(image__isnull=False)

    for data in allData:
        gcp_data = json.loads(data.gcp_data)
        gcp_data = gcp_data['text_annotations']
        texts = [text['description'] for text in gcp_data]
        # print(texts)
        regex = r"(?:Country\s*of\s*Origin|countryofOrigin|made|assembled)\s*(?:in|of|:)?\s*([A-Za-z\s]+)"
        for text in texts:
            # re.IGNORECASE makes the search case-insensitive
            match = re.search(regex, text, re.IGNORECASE)
            if match:
                return 1
    return 0
