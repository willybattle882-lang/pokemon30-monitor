import json
from .models import Product

def load_catalog(path="data/catalog.json"):
    with open(path, encoding="utf-8") as f:
        data=json.load(f)
    return [Product(**p) for p in data["products"]]
