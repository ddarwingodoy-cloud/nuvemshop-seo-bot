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
    access_token = os.environ.get("NUVEMSHOP_ACCESS_TOKEN")
    store_id = os.environ.get("NUVEMSHOP_STORE_ID")

    headers = {
        "Authentication": f"bearer {access_token}",
        "User-Agent": "nuvemshop-seo-bot"
    }

    url = f"https://api.tiendanube.com/v1/{store_id}/categories"

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

@app.route("/atualizar-categoria")
def atualizar_categoria():
    access_token = os.environ.get("NUVEMSHOP_ACCESS_TOKEN")
    store_id = os.environ.get("NUVEMSHOP_STORE_ID")

    headers = {
    "Authentication": f"bearer {access_token}",
    "User-Agent": "nuvemshop-seo-bot",
    "Content-Type": "application/json"
}

    categoria_id = 37845299

    url = f"https://api.tiendanube.com/v1/{store_id}/categories/{categoria_id}"

    payload = {
        "name": {
            "pt": "Teste SEO"
        },
        "description": {
            "pt": "Categoria de teste"
        },
        "seo_title": {
            "pt": "Teste SEO | Ceramicando"
        },
        "seo_description": {
            "pt": "Categoria de teste para validar atualização de SEO via API na Nuvemshop."
        }
    }

    response = requests.put(url, headers=headers, json=payload)

    return response.text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
