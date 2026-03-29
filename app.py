from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BASE_URL = "https://api.tiendanube.com/2025-03"


def get_env_credentials():
    access_token = os.environ.get("NUVEMSHOP_ACCESS_TOKEN")
    store_id = os.environ.get("NUVEMSHOP_STORE_ID")

    if not access_token or not store_id:
        return None, None

    return access_token, store_id


def get_headers(access_token: str) -> dict:
    return {
        "Authentication": f"bearer {access_token}",
        "User-Agent": "SEO Categories Automation (ddarwingodoy@gmail.com)",
        "Content-Type": "application/json; charset=utf-8"
    }


def merge_translations(current: dict, updates: dict) -> dict:
    """
    Preserva os valores existentes e só sobrescreve os idiomas enviados.
    Ignora valores vazios.
    """
    merged = dict(current or {})

    for lang, value in updates.items():
        if value is not None and value != "":
            merged[lang] = value

    return merged


@app.route("/")
def home():
    return "App rodando"


@app.route("/categorias")
def listar_categorias():
    access_token, store_id = get_env_credentials()

    if not access_token or not store_id:
        return jsonify({"error": "Variáveis NUVEMSHOP_ACCESS_TOKEN ou NUVEMSHOP_STORE_ID não configuradas"}), 500

    url = f"{BASE_URL}/{store_id}/categories"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)

    return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/categoria/<int:categoria_id>")
def get_categoria(categoria_id: int):
    access_token, store_id = get_env_credentials()

    if not access_token or not store_id:
        return jsonify({"error": "Variáveis NUVEMSHOP_ACCESS_TOKEN ou NUVEMSHOP_STORE_ID não configuradas"}), 500

    url = f"{BASE_URL}/{store_id}/categories/{categoria_id}"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)

    return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/atualizar-categoria/<int:categoria_id>")
def atualizar_categoria(categoria_id: int):
    access_token, store_id = get_env_credentials()

    if not access_token or not store_id:
        return jsonify({"error": "Variáveis NUVEMSHOP_ACCESS_TOKEN ou NUVEMSHOP_STORE_ID não configuradas"}), 500

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/categories/{categoria_id}"

    # 1. Lê a categoria atual
    get_response = requests.get(url, headers=headers, timeout=30)

    if get_response.status_code != 200:
        return get_response.text, get_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    categoria_atual = get_response.json()

    # 2. Captura parâmetros recebidos pela URL
    updates_name = {
        "pt": request.args.get("name_pt"),
        "es": request.args.get("name_es"),
        "en": request.args.get("name_en"),
    }

    updates_description = {
        "pt": request.args.get("description_pt"),
        "es": request.args.get("description_es"),
        "en": request.args.get("description_en"),
    }

    updates_handle = {
        "pt": request.args.get("handle_pt"),
        "es": request.args.get("handle_es"),
        "en": request.args.get("handle_en"),
    }

    updates_seo_title = {
        "pt": request.args.get("seo_title_pt"),
        "es": request.args.get("seo_title_es"),
        "en": request.args.get("seo_title_en"),
    }

    updates_seo_description = {
        "pt": request.args.get("seo_description_pt"),
        "es": request.args.get("seo_description_es"),
        "en": request.args.get("seo_description_en"),
    }

    # 3. Preserva o que já existe e atualiza só o que veio na URL
    payload = {
        "name": merge_translations(categoria_atual.get("name", {}), updates_name),
        "description": merge_translations(categoria_atual.get("description", {}), updates_description),
        "handle": merge_translations(categoria_atual.get("handle", {}), updates_handle),
        "seo_title": merge_translations(categoria_atual.get("seo_title", {}), updates_seo_title),
        "seo_description": merge_translations(categoria_atual.get("seo_description", {}), updates_seo_description),
    }

    # 4. Atualiza a categoria
    put_response = requests.put(url, headers=headers, json=payload, timeout=30)

    return put_response.text, put_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    # 4. Organizando o Json
@app.route("/categoria-revisao/<int:categoria_id>")
def categoria_revisao(categoria_id: int):
    access_token, store_id = get_env_credentials()

    if not access_token or not store_id:
        return jsonify({"error": "Variáveis NUVEMSHOP_ACCESS_TOKEN ou NUVEMSHOP_STORE_ID não configuradas"}), 500

    url = f"{BASE_URL}/{store_id}/categories/{categoria_id}"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)

    if response.status_code != 200:
        return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    categoria = response.json()

    revisao = {
        "id": categoria.get("id"),
        "name": {
            "pt": categoria.get("name", {}).get("pt", ""),
            "es": categoria.get("name", {}).get("es", ""),
            "en": categoria.get("name", {}).get("en", "")
        },
        "handle": {
            "pt": categoria.get("handle", {}).get("pt", ""),
            "es": categoria.get("handle", {}).get("es", ""),
            "en": categoria.get("handle", {}).get("en", "")
        },
        "description": {
            "pt": categoria.get("description", {}).get("pt", ""),
            "es": categoria.get("description", {}).get("es", ""),
            "en": categoria.get("description", {}).get("en", "")
        },
        "seo_title": {
            "pt": categoria.get("seo_title", {}).get("pt", ""),
            "es": categoria.get("seo_title", {}).get("es", ""),
            "en": categoria.get("seo_title", {}).get("en", "")
        },
        "seo_description": {
            "pt": categoria.get("seo_description", {}).get("pt", ""),
            "es": categoria.get("seo_description", {}).get("es", ""),
            "en": categoria.get("seo_description", {}).get("en", "")
        }
    }

    return jsonify(revisao)

    # 4. Json Estruturado
@app.route("/atualizar-categoria-json/<int:categoria_id>", methods=["POST"])
def atualizar_categoria_json(categoria_id: int):
    access_token, store_id = get_env_credentials()

    if not access_token or not store_id:
        return jsonify({"error": "Variáveis NUVEMSHOP_ACCESS_TOKEN ou NUVEMSHOP_STORE_ID não configuradas"}), 500

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/categories/{categoria_id}"

    # 1. Lê a categoria atual
    get_response = requests.get(url, headers=headers, timeout=30)

    if get_response.status_code != 200:
        return get_response.text, get_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    categoria_atual = get_response.json()

    # 2. Lê o JSON enviado
    body = request.get_json(silent=True) or {}

    payload = {
        "name": merge_translations(
            categoria_atual.get("name", {}),
            body.get("name", {})
        ),
        "description": merge_translations(
            categoria_atual.get("description", {}),
            body.get("description", {})
        ),
        "handle": merge_translations(
            categoria_atual.get("handle", {}),
            body.get("handle", {})
        ),
        "seo_title": merge_translations(
            categoria_atual.get("seo_title", {}),
            body.get("seo_title", {})
        ),
        "seo_description": merge_translations(
            categoria_atual.get("seo_description", {}),
            body.get("seo_description", {})
        ),
    }

    # 3. Atualiza
    put_response = requests.put(url, headers=headers, json=payload, timeout=30)

    return put_response.text, put_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

# 🔹 LISTAR PRODUTOS
@app.route("/produtos")
def listar_produtos():
    access_token, store_id = get_env_credentials()

    url = f"{BASE_URL}/{store_id}/products"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)

    return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}


# 🔹 PRODUTO POR ID
@app.route("/produto/<int:produto_id>")
def get_produto(produto_id: int):
    access_token, store_id = get_env_credentials()

    url = f"{BASE_URL}/{store_id}/products/{produto_id}"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)

    return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}


# 🔹 PRODUTO PARA REVISÃO
@app.route("/produto-revisao/<int:produto_id>")
def produto_revisao(produto_id: int):
    access_token, store_id = get_env_credentials()

    url = f"{BASE_URL}/{store_id}/products/{produto_id}"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)

    if response.status_code != 200:
        return response.text, response.status_code

    produto = response.json()

    revisao = {
        "id": produto.get("id"),
        "name": produto.get("name", {}),
        "description": produto.get("description", {}),
        "seo_title": produto.get("seo_title", {}),
        "seo_description": produto.get("seo_description", {}),
        "handle": produto.get("handle", {})
    }

    return jsonify(revisao)


# 🔹 ATUALIZAR PRODUTO
@app.route("/atualizar-produto-json/<int:produto_id>", methods=["POST"])
def atualizar_produto_json(produto_id: int):
    access_token, store_id = get_env_credentials()

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/products/{produto_id}"

    # lê atual
    get_response = requests.get(url, headers=headers, timeout=30)
    produto_atual = get_response.json()

    body = request.get_json(silent=True) or {}

    payload = {
        "name": merge_translations(produto_atual.get("name", {}), body.get("name", {})),
        "description": merge_translations(produto_atual.get("description", {}), body.get("description", {})),
        "handle": merge_translations(produto_atual.get("handle", {}), body.get("handle", {})),
        "seo_title": merge_translations(produto_atual.get("seo_title", {}), body.get("seo_title", {})),
        "seo_description": merge_translations(produto_atual.get("seo_description", {}), body.get("seo_description", {})),
    }

    put_response = requests.put(url, headers=headers, json=payload, timeout=30)

    return put_response.text, put_response.status_code

# 🔹 ENDPOINT PREVIEW
@app.route("/preview-categoria-json/<int:categoria_id>", methods=["POST"])
def preview_categoria_json(categoria_id: int):
    access_token, store_id = get_env_credentials()

    if not access_token or not store_id:
        return jsonify({"error": "Variáveis NUVEMSHOP_ACCESS_TOKEN ou NUVEMSHOP_STORE_ID não configuradas"}), 500

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/categories/{categoria_id}"

    # 1. Lê a categoria atual
    get_response = requests.get(url, headers=headers, timeout=30)

    if get_response.status_code != 200:
        return get_response.text, get_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    categoria_atual = get_response.json()

    # 2. Lê o JSON enviado
    body = request.get_json(silent=True) or {}

    preview = {
        "id": categoria_atual.get("id"),
        "antes": {
            "name": categoria_atual.get("name", {}),
            "description": categoria_atual.get("description", {}),
            "handle": categoria_atual.get("handle", {}),
            "seo_title": categoria_atual.get("seo_title", {}),
            "seo_description": categoria_atual.get("seo_description", {})
        },
        "depois": {
            "name": merge_translations(
                categoria_atual.get("name", {}),
                body.get("name", {})
            ),
            "description": merge_translations(
                categoria_atual.get("description", {}),
                body.get("description", {})
            ),
            "handle": merge_translations(
                categoria_atual.get("handle", {}),
                body.get("handle", {})
            ),
            "seo_title": merge_translations(
                categoria_atual.get("seo_title", {}),
                body.get("seo_title", {})
            ),
            "seo_description": merge_translations(
                categoria_atual.get("seo_description", {}),
                body.get("seo_description", {})
            )
        }
    }

    return jsonify(preview)

# 🔹 PREVIEW PRODUTOS
@app.route("/preview-produto-json/<int:produto_id>", methods=["POST"])
def preview_produto_json(produto_id: int):
    access_token, store_id = get_env_credentials()

    if not access_token or not store_id:
        return jsonify({"error": "Variáveis NUVEMSHOP_ACCESS_TOKEN ou NUVEMSHOP_STORE_ID não configuradas"}), 500

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/products/{produto_id}"

    # 1. Lê o produto atual
    get_response = requests.get(url, headers=headers, timeout=30)

    if get_response.status_code != 200:
        return get_response.text, get_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    produto_atual = get_response.json()

    # 2. Lê o JSON enviado
    body = request.get_json(silent=True) or {}

    preview = {
        "id": produto_atual.get("id"),
        "antes": {
            "name": produto_atual.get("name", {}),
            "description": produto_atual.get("description", {}),
            "handle": produto_atual.get("handle", {}),
            "seo_title": produto_atual.get("seo_title", {}),
            "seo_description": produto_atual.get("seo_description", {})
        },
        "depois": {
            "name": merge_translations(
                produto_atual.get("name", {}),
                body.get("name", {})
            ),
            "description": merge_translations(
                produto_atual.get("description", {}),
                body.get("description", {})
            ),
            "handle": merge_translations(
                produto_atual.get("handle", {}),
                body.get("handle", {})
            ),
            "seo_title": merge_translations(
                produto_atual.get("seo_title", {}),
                body.get("seo_title", {})
            ),
            "seo_description": merge_translations(
                produto_atual.get("seo_description", {}),
                body.get("seo_description", {})
            )
        }
    }

    return jsonify(preview)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
