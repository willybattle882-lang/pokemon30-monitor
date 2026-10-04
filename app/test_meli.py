from .meli import MercadoLivreClient

client = MercadoLivreClient()

results = client.search("Pokemon", limit=5)

for item in results:
    print("=" * 60)
    print(f"ID:       {item.item_id}")
    print(f"Nome:     {item.title}")
    print(f"Preço:    R$ {item.price:.2f}")
    print(f"Condição: {item.condition}")
    print(f"Frete:    {item.shipping_cost}")
    print(f"Link:     {item.permalink}")