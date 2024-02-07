from catalogue.models.products import Product
from catalogue.models.attributes import Attribute
from catalogue.models.relations import ProductAttribute
import requests
import json

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
    product_fssai_number = ProductAttribute.objects.filter(attribute=attribute).first()
    if product_fssai_number is None:
        return None
    else:
        flrsLicenseNo = product_fssai_number.value
        response = requests.post(
            f"https://foscos.fssai.gov.in/gateway/commonauth/commonapi/getadvancesearchapplicationdetails/1", 
            {"flrsLicenseNo":flrsLicenseNo}
            )
        obj = json.loads(response.text)
        return obj
    
def check_isi_standard_logo(product):
    pass

def check_mrp(product):
    pass

def check_manufacturer(product):
    pass

def check_ingredients(product):
    pass

def check_care_details(product):
    pass

def check_mfg_date(product):
    pass

