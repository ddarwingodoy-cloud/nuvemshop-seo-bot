from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔹 HOME
@app.route("/")
def home():
    return "App rodando 🚀"


# 🔹 CALLBACK (gera o access_token)
@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return "Code não encontrado"

    url = "https://www.tiendanube.com/apps/authorize/token"

    payload = {
        "client_id": os.environ.get("NUVEMSHOP_APP_ID"),
        "client_secret": os.environ.get("NUVEMSHOP_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code
    }

    response = requests.post(url, json=payload)

    return response.text


# 🔹 TESTE 1: DADOS DA LOJA (descobrir store_id)
@app.route("/loja")
def loja():
    access_token = "df71a2fdbd57e5b7354c882c6a7f1680ede19a56"

    headers = {
        "Authentication": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = "https://api.tiendanube.com/v1/store"

    response = requests.get(url, headers=headers)

    return response.text


# 🔹 TESTE 2: CATEGORIAS (usar depois que tiver store_id)
@app.route("/categorias")
def categorias():
    access_token = "df71a2fdbd57e5b7354c882c6a7f1680ede19a56"
    store_id = "7487712"

    headers = {
        "Authentication": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = f"https://api.tiendanube.com/v1/{store_id}/categories"

    response = requests.get(url, headers=headers)

    return response.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
