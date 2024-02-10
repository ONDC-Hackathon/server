from catalogue.models.rules import *
from importlib import import_module


def calculate_compliance_score(product):
    try:
        rules = Rule.objects.filter(category=product.category)
        rules.union(rules, Rule.objects.filter(
            sub_category=product.sub_category))
        rules.union(rules, Rule.objects.filter(variant=product.variant))
        files = rules.values('file')
        score = 0
        for file in files:
            try:
                rule = import_module("rules."+str(file['file'])[:-3])
                score += rule.calculate(product)
            except Exception as e:
                print(e)
                continue
        return score/rules.count()
    except Exception as e:
        print(e)
        return 0
