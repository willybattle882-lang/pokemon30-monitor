import requests

class Telegram:
    def __init__(self,token,chat):
        self.token,self.chat=token,chat
    def send(self,text):
        if not self.token or not self.chat:
            raise RuntimeError("Configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID")
        r=requests.post(f"https://api.telegram.org/bot{self.token}/sendMessage",
                        json={"chat_id":self.chat,"text":text,"disable_web_page_preview":False},timeout=20)
        r.raise_for_status()

def money(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def alert_text(l,p,ratio,limit):
    shipping=money(l.shipping_cost) if l.shipping_cost is not None else "consultar no anúncio"
    packs=f"\n📦 Boosters: {p.packs}" if p.packs else ""
    return (f"🚨 OPORTUNIDADE — Pokémon 30 Anos\n\n"
            f"🎴 {p.name}\n💰 Preço: {money(l.price)}\n"
            f"🏷️ Sugerido: {money(p.suggested_price)}\n"
            f"📊 {ratio*100:.1f}% do sugerido\n"
            f"📏 Limite: {money(limit)}{packs}\n"
            f"🚚 Frete: {shipping}\n\n"
            f"🆔 {l.item_id}\n🔗 {l.permalink}")
