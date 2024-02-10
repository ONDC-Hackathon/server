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
    date_patterns = [
        r"\b(?:19|20)\d\d[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12][0-9]|3[01])\b",
        r"\b(0[1-9]|1[0-2])[-/](0[1-9]|[12][0-9]|3[01])[-/](?:19|20)\d\d\b",
        r"\b(0[1-9]|[12][0-9]|3[01])\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(19|20)\d\d\b",
        r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(0[1-9]|[12][0-9]|3[01]),\s+(19|20)\d\d\b"
    ]
    for text in texts:
        # re.IGNORECASE makes the search case-insensitive
        for pattern in date_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 1
    return 0
