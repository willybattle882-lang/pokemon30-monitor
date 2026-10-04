import os
import secrets
import requests

from flask import Flask, redirect, request

from .token_store import save_token


app = Flask(__name__)

BASE_AUTH = "https://auth.mercadolivre.com.br/authorization"
BASE_API = "https://api.mercadolibre.com"

REDIRECT_URI = "https://pokemon30-monitor.onrender.com/oauth/callback"

_oauth_state = None


@app.route("/oauth/login")
def oauth_login():
    global _oauth_state

    _oauth_state = secrets.token_urlsafe(32)

    url = (
        f"{BASE_AUTH}"
        f"?response_type=code"
        f"&client_id={os.environ['MELI_CLIENT_ID']}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={_oauth_state}"
    )

    return redirect(url)


@app.route("/oauth/callback")
def oauth_callback():
    global _oauth_state

    code = request.args.get("code")
    state = request.args.get("state")

    if not code:
        return "Erro: Mercado Livre não enviou o code.", 400

    if state != _oauth_state:
        return "Erro: state inválido.", 400

    response = requests.post(
        f"{BASE_API}/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": os.environ["MELI_CLIENT_ID"],
            "client_secret": os.environ["MELI_CLIENT_SECRET"],
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        timeout=20,
    )

    if not response.ok:
        return (
            f"Erro ao obter token: {response.status_code}<br>"
            f"{response.text}"
        ), 500

    token_data = response.json()

    save_token(token_data)

    print("Mercado Livre autorizado com sucesso.")
    print("Token salvo.")

    return """
    <h1>Mercado Livre autorizado!</h1>
    <p>Autorização concluída com sucesso.</p>
    <p>O token foi salvo.</p>
    """


@app.route("/")
def home():
    return "Pokémon 30 Anos Monitor online."


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000"))
    )