import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    telegram_bot_token: str
    telegram_chat_id: str
    price_limit_ratio: float
    poll_seconds: int
    search_terms: list[str]
    meli_access_token: str | None

def get_config():
    return Config(
        os.getenv("TELEGRAM_BOT_TOKEN","").strip(),
        os.getenv("TELEGRAM_CHAT_ID","").strip(),
        float(os.getenv("PRICE_LIMIT_RATIO","1.10")),
        int(os.getenv("POLL_SECONDS","600")),
        [x.strip() for x in os.getenv("SEARCH_TERMS","").split("|") if x.strip()],
        os.getenv("MELI_ACCESS_TOKEN","").strip() or None
    )
