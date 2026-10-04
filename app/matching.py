import re, unicodedata
from rapidfuzz.fuzz import token_set_ratio
from .models import Listing, Product

def norm(s):
    s=unicodedata.normalize("NFKD",s.lower())
    s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9]+"," ",s)).strip()

def match(listing, products):
    title=norm(listing.title)
    found=[]
    for p in products:
        if p.suggested_price is None: continue
        score=max([token_set_ratio(norm(x),title) for x in [p.name]+p.aliases] or [0])
        if score>=72:
            found.append((score,p))
    return max(found,key=lambda x:x[0]) if found else None
