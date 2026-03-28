from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "App rodando"

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

    return f"Resposta da API: {response.text}"


# 👇 NOVO ENDPOINT PARA PEGAR STORE_ID
@app.route("/loja")
def dados_loja():
    access_token = "COLE_AQUI_SEU_TOKEN"

    headers = {
        "Authentication": f"bearer {access_token}"
    }

    url = "https://api.tiendanube.com/v1/store"

    response = requests.get(url, headers=headers)

    return response.text


# 👇 CATEGORIAS (ainda com placeholder)
@app.route("/categorias")
def listar_categorias():
    access_token = "df71a2fdbd57e5b7354c882c6a7f1680ede19a56"

    headers = {
        "Authentication": f"bearer {access_token}"
    }

    url = "https://api.tiendanube.com/v1/SEU_STORE_ID/categories"

    response = requests.get(url, headers=headers)

    return response.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
