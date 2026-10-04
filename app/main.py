import time, logging
from .config import get_config
from .catalog import load_catalog
from .meli import MercadoLivreClient
from .matching import match
from .db import DB
from .telegram import Telegram, alert_text

logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s")

def scan():
    cfg=get_config()
    products=load_catalog()
    db=DB()
    meli=MercadoLivreClient(cfg.meli_access_token)
    tg=Telegram(cfg.telegram_bot_token,cfg.telegram_chat_id)
    done=set()
    for q in cfg.search_terms:
        try:
            listings=meli.search(q)
        except Exception:
            logging.exception("Falha na busca %s",q); continue
        for l in listings:
            if l.item_id in done: continue
            done.add(l.item_id)
            m=match(l,products)
            if not m: continue
            _,p=m
            limit=p.suggested_price*cfg.price_limit_ratio
            if l.price<=0 or l.price>limit or db.alerted(l.item_id): continue
            tg.send(alert_text(l,p,l.price/p.suggested_price,limit))
            db.add(l.item_id,l.price,p.id)
            logging.info("Alerta enviado: %s",l.item_id)

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--once",action="store_true")
    a=ap.parse_args()
    cfg=get_config()
    if a.once: scan()
    else:
        while True:
            scan()
            time.sleep(cfg.poll_seconds)
