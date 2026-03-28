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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
