from dataclasses import dataclass

@dataclass
class Listing:
    item_id: str
    title: str
    price: float
    currency: str
    permalink: str
    seller_id: int | None = None
    condition: str | None = None
    shipping_cost: float | None = None
    official_store_id: int | None = None

@dataclass
class Product:
    id: str
    name: str
    aliases: list[str]
    suggested_price: float | None
    packs: int | None = None
