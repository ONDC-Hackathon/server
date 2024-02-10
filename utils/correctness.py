from catalogue.models.products import Product
from catalogue.models.attributes import Attribute
from catalogue.models.relations import ProductAttribute
import requests
import json
from bs4 import BeautifulSoup
import time
import random
from utils.colorScore import find_closest_color_score


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


def get_fssai_license_details(product):
    attribute = Attribute.objects.get(title="fssai number")
    licenseno = ProductAttribute.objects.filter(
        product=product).filter(attribute=attribute).first().value
    data = [element for element in MOCK_DATA if element['licenseno'] == licenseno][0]
    return data


def check_color(product):
    color = product.attributes.all().filter(attribute__title="color").first().value
    print(color)
    if not color:
        return 0  # if color is not mentioned
    gcp_data_raw = product.attribute_logs.all().filter(
        product=product).first().gcp_data
    gcp_data = json.loads(gcp_data_raw)
    # print(gcp_data['image_properties_annotation'])
    return find_closest_color_score(color, gcp_data['image_properties_annotation']['dominant_colors'])


def check_brand(product):
    product = product.attributes.all().filter(
        attribute__title="brand").first().value
    if not product:
        return 0
    else:
        return 1


def check_country_of_origin(product):
    if product.attributes.all().filter(attribute__title="country of origin").first().value:
        return 1
    else:
        return 0


def check_revelance_of_subcategory_with_image(product):
    sub_category = product.sub_category
    print(sub_category)
    return 1


def calculate_correctness_score(product):
    correctness_score = 0
    correctness_score += check_color(product)
    correctness_score += check_brand(product)
    correctness_score += check_country_of_origin(product)
    correctness_score += check_revelance_of_subcategory_with_image(product)
    return correctness_score/4
