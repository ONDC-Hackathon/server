from catalogue.models.products import Product
from catalogue.models.attributes import Attribute
from catalogue.models.relations import ProductAttribute
import requests
import json
from bs4 import BeautifulSoup
import time
import random
import re
from utils.colorScore import find_closest_color_score
from utils.similarityIndex import *

MOCK_DATA = [
    {
        "premiseaddress": "Ludhiana Beverages Pvt. Ltd., Unit-2. Village Jaspalon, Teh Khanna, Near Doraha",
        "licenseno": "10012063000047",
        "fboid": 66428527,
        "displayrefid": "10230620104872182",
        "licensecategoryname": "Central License",
        "statename": "Punjab",
        "statusdesc": "License Issued",
        "licensecategoryid": 1,
        "talukname": "Ludhiana-4(P/S Khanna, Payal, Samrala, Doraha, Dehlon, Machhiwara, Maloud)",
        "districtname": "Ludhiana",
        "companyname": "Ludhiana Beverages Pvt. Ltd., Unit-2",
        "licenseactiveflag": True,
        "refid": 104872182,
        "apptypedesc": "Modification",
        "villagename": None,
        "premisepincode": 141421,
        "product_list": [
            "Packaged Drinking Water (other than Mineral Water)",
            "Carbonated Water",
            "Synthetic Syrup for use in Dispensers for Carbonated Water",
            "Caffeinated Beverage",
            "Carbonated Fruit Beverages or Fruit Drinks",
        ]
    },
    {
        "premiseaddress": "27/3 CAUVERY ROAD\n",
        "licenseno": "10013042001080",
        "fboid": 65728274,
        "displayrefid": "10231101105280457",
        "licensecategoryname": "Central License",
        "statename": "Tamil Nadu",
        "statusdesc": "License Issued",
        "licensecategoryid": 1,
        "talukname": "Trichy  Corporation  Ward-8",
        "districtname": "Tiruchirappalli",
        "companyname": "LION DATES IMPEX PVT LTD",
        "licenseactiveflag": True,
        "refid": 105280457,
        "apptypedesc": "Modification",
        "villagename": None,
        "premisepincode": 620002,
        "product_list": [
            "CHOCODATE WITH BADAM ",
            "LION DATES HEALTH MIX",
            "LION DATES HALWA ",
            "Jams, Fruit Jellies and Marmalades",
            "Tamarind Pulp\/Puree and Concentrate",
            "Honey",
            "Fruits\/Vegetable Sauces ",
            "Thermally Processed Fruit Beverages \/ Fruit Drink\/ Ready to Serve Fruit Beverages",
            "Squash ",
            "Fruit Syrup\/ Fruit Sharbats",
            "Dates",
            "Dry fruits and Nuts",
            "Rolled Oats",
            "Breakfast Cereal",
            "Dehydrated Fruits",
            "Peeled or cut, minimally processed fruit"
        ]
    }
]


def get_bis_details_for_electronics(product):
    try:
        attribute = Attribute.objects.get(title="registration number")
        product_registration_number = ProductAttribute.objects.filter(
            attribute=attribute).first()
        if product_registration_number is None:
            return None
        else:
            r_no = product_registration_number.value
            response = requests.get(
                f"https://www.manakonline.in/MANAK/BISCRS.do?rno={r_no}")
            response = response.text.strip("\"").replace("\\", "")
            response = "[" + response + "]"
            data = json.loads(response)
            obj = data[0]
            return obj
    except Exception as e:
        print(e)
        return {}


def check_color(product):
    try:
        color = product.attributes.all().filter(attribute__title="color").first().value
        print(color)
        if not color:
            return 0  # if color is not mentioned
        allData = product.attribute_logs.all().filter(image__isnull=False)
        cnt = 0
        score = 0
        for data in allData:
            gcp_data_raw = data.gcp_data
            gcp_data = json.loads(gcp_data_raw)
            score += find_closest_color_score(
                color, gcp_data['image_properties_annotation']['dominant_colors'])
            cnt += 1

        if (cnt == 0):
            return 0
        return score/cnt
    except Exception as e:
        print(e)
        return 0


def check_brand(product):
    try:
        product = product.attributes.all().filter(
            attribute__title="brand").first().value
        if not product:
            return 0
        else:
            return 1
    except Exception as e:
        print(e)
        return 0


def check_country_of_origin(product):
    try:
        if product.attributes.all().filter(attribute__title="country of origin").first().value:
            return 1
        else:
            return 0
    except Exception as e:
        print(e)
        return 0


def check_revelance_of_subcategory_with_image(product):
    try:
        sub_category = product.sub_category.title
        allData = product.attribute_logs.all().filter(image__isnull=False)
        cnt = 0
        score = 0
        pattern = re.escape(sub_category).replace(r'\ ', '[- ]?')
        # from web entities
        for data in allData:
            gcp_data_raw = data.gcp_data
            gcp_data = json.loads(gcp_data_raw)
            web_entities = gcp_data['web_detection']['web_entities']
            for x in web_entities:
                print(x['description'])
                if re.search(pattern, x['description'], re.IGNORECASE):
                    score += x['score']
                    cnt += 1.0
        # from labels
        for data in allData:
            gcp_data_raw = data.gcp_data
            gcp_data = json.loads(gcp_data_raw)
            labels = gcp_data['label_annotations']
            for x in labels:
                if re.search(pattern, x['description'], re.IGNORECASE):
                    score += x['score']
                    cnt += 1.0

        if (cnt == 0):
            return 0
        print("score", score, "cnt", cnt)
        return min((score/cnt), 1)
    except Exception as e:
        print("Error in check_revelance_of_subcategory_with_image", e)
        return 0


def check_registration_number(product):
    try:
        if product.category.title == "Electronics":
            bis_data = get_bis_details_for_electronics(product)
            # obj = {
            #     "title": product.title,
            #     "brand": product.brand,
            #     "manufacturer": product.manufacturer,
            #     "about": product.about,
            # }
            str1 = f"{product.title} {product.brand} {product.manufacturer} {product.about}"
            str2 = ""
            for data in bis_data.values():
                str2 += f" {data}"
            score = overall_similarity_score_between_text(str1, str2)

            return max(0.33, score)
        elif product.category.title == "Food":
            obj = {
                "title": product.title,
                "brand": product.brand,
                "manufacturer": product.manufacturer,
                "about": product.about,
            }
            str1 = f"{product.title} {product.brand} {product.manufacturer} {product.about}"
            str2 = ""
            for data in random.choice(MOCK_DATA).values():
                str2 = f"{ data}"
            score = overall_similarity_score_between_text(str1, str2)
            return score
    except Exception as e:
        print(e)
        print("Error in check_registration_number")
        return 0


COLOR_SCORE_WEIGHT = 0.1
BRAND_SCORE_WEIGHT = 0.05
COUNTRY_OF_ORIGIN_SCORE_WEIGHT = 0.05
SUBCATEGORY_SCORE_WEIGHT = 0.5
REGISTRATION_SCORE_WEIGHT = 0.3


def calculate_correctness_score(product):
    try:
        correctness_score = 0

        color_score = check_color(product)
        brand_score = check_brand(product)
        country_of_origin_score = check_country_of_origin(product)
        subcategory_score = check_revelance_of_subcategory_with_image(product)
        registration_score = check_registration_number(product)
        print(f"Color score: {color_score}")
        print(f"Brand score: {brand_score}")
        print(f"Country of origin score: {country_of_origin_score}")
        print(f"Subcategory score: {subcategory_score}")
        print(f"Registration score: {registration_score}")

        correctness_score += color_score*COLOR_SCORE_WEIGHT
        correctness_score += brand_score*BRAND_SCORE_WEIGHT
        correctness_score += country_of_origin_score*COUNTRY_OF_ORIGIN_SCORE_WEIGHT
        correctness_score += subcategory_score*SUBCATEGORY_SCORE_WEIGHT
        correctness_score += registration_score*REGISTRATION_SCORE_WEIGHT

        return correctness_score
    except Exception as e:
        print(e)
        return 0
