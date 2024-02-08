from catalogue.models.products import Product
from catalogue.models.attributes import Attribute
from catalogue.models.relations import ProductAttribute
import requests
import json
from bs4 import BeautifulSoup
import time
import random



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
    product_registration_number = ProductAttribute.objects.filter(attribute=attribute).first()
    if product_registration_number is None:
        return None
    else:
        r_no = product_registration_number.value
        response = requests.get(f"https://www.manakonline.in/MANAK/BISCRS.do?rno={r_no}")
        response = response.text.strip("\"").replace("\\","") 
        response = "[" + response + "]"
        data = json.loads(response) 
        obj = data[0]
        return obj
        
def get_fssai_license_details(product):
    attribute = Attribute.objects.get(title="fssai number")
    licenseno = ProductAttribute.objects.filter(product=product).filter(attribute=attribute).first().value
    data = [element for element in MOCK_DATA if element['licenseno'] == licenseno][0]
    return data
