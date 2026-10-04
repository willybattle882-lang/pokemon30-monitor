import json
from pathlib import Path


TOKEN_FILE = Path("data/meli_token.json")


def save_token(token_data):
    TOKEN_FILE.parent.mkdir(exist_ok=True)

    data = {
        "access_token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token"),
        "expires_in": token_data.get("expires_in"),
        "user_id": token_data.get("user_id"),
    }

    TOKEN_FILE.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )


def load_token():
    if not TOKEN_FILE.exists():
        return None

    try:
        return json.loads(
            TOKEN_FILE.read_text(encoding="utf-8")
        )
    except Exception:
        return None