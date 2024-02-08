from catalogue.models.rules import *
from importlib import import_module

def calculate_compliance_score(product):
    rules = Rule.objects.filter(category=product.category)
    rules.union(rules, Rule.objects.filter(sub_category=product.sub_category))
    rules.union(rules, Rule.objects.filter(variant=product.variant))
    files = rules.values('file')
    score = 0
    for file in files:
        rule = import_module("rules."+str(file['file'])[:-3])
        score += rule.calculate(product)
    return score/rules.count()
    






