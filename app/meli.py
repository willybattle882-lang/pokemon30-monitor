import requests
from .models import Listing

BASE="https://api.mercadolibre.com"

class MercadoLivreClient:
    def __init__(self, access_token=None):
        self.s=requests.Session()
        self.s.headers["User-Agent"]="pokemon30-monitor/0.1"
        if access_token:
            self.s.headers["Authorization"]=f"Bearer {access_token}"

    def search(self, query, limit=50):
        r=self.s.get(f"{BASE}/sites/MLB/search",
                     params={"q":query,"limit":min(limit,50),"sort":"date_desc"},
                     timeout=20)
        r.raise_for_status()
        out=[]
        for x in r.json().get("results",[]):
            shipping=x.get("shipping") or {}
            out.append(Listing(
                item_id=x.get("id",""),
                title=x.get("title",""),
                price=float(x.get("price") or 0),
                currency=x.get("currency_id","BRL"),
                permalink=x.get("permalink",""),
                seller_id=(x.get("seller") or {}).get("id"),
                condition=x.get("condition"),
                shipping_cost=shipping.get("cost") if isinstance(shipping,dict) else None,
                official_store_id=x.get("official_store_id")
            ))
        return [x for x in out if x.item_id and x.permalink]
