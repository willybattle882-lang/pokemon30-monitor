from .config import get_config
from .telegram import Telegram
if __name__=="__main__":
    c=get_config()
    Telegram(c.telegram_bot_token,c.telegram_chat_id).send("✅ Pokémon 30 Anos Monitor: Telegram OK.")
