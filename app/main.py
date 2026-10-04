```python
import os
import time
import logging
import threading

from .config import get_config
from .catalog import load_catalog
from .meli import MercadoLivreClient
from .matching import match
from .db import DB
from .telegram import Telegram, alert_text
from .oauth import app as oauth_app


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def scan():
    cfg = get_config()
    products = load_catalog()
    db = DB()
    meli = MercadoLivreClient(cfg.meli_access_token)
    tg = Telegram(
        cfg.telegram_bot_token,
        cfg.telegram_chat_id
    )

    done = set()

    for q in cfg.search_terms:
        try:
            listings = meli.search(q)
        except Exception:
            logging.exception("Falha na busca %s", q)
            continue

        for l in listings:
            if l.item_id in done:
                continue

            done.add(l.item_id)

            m = match(l, products)
            if not m:
                continue

            _, p = m

            limit = p.suggested_price * cfg.price_limit_ratio

            if (
                l.price <= 0
                or l.price > limit
                or db.alerted(l.item_id)
            ):
                continue

            tg.send(
                alert_text(
                    l,
                    p,
                    l.price / p.suggested_price,
                    limit
                )
            )

            db.add(
                l.item_id,
                l.price,
                p.id
            )

            logging.info(
                "Alerta enviado: %s",
                l.item_id
            )


def monitor_loop():
    cfg = get_config()

    while True:
        try:
            scan()
        except Exception:
            logging.exception(
                "Erro durante o monitoramento"
            )

        time.sleep(cfg.poll_seconds)


# Inicia o monitor em segundo plano.
# Isso permite que o Gunicorn mantenha o Flask
# disponível para o OAuth.
monitor_thread = threading.Thread(
    target=monitor_loop,
    daemon=True
)

monitor_thread.start()


if __name__ == "__main__":
    port = int(
        os.environ.get("PORT", "10000")
    )

    oauth_app.run(
        host="0.0.0.0",
        port=port
    )
```
