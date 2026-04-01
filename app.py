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

    return access_token.strip(), str(store_id).strip()


def get_headers(access_token: str) -> dict:
    return {
        "Authentication": f"bearer {access_token}",
        "User-Agent": "SEO Categories Automation (ddarwingodoy@gmail.com)",
        "Content-Type": "application/json"
    }


def error_if_missing_credentials(access_token, store_id):
    if not access_token or not store_id:
        return jsonify({
            "error": "Variáveis NUVEMSHOP_ACCESS_TOKEN ou NUVEMSHOP_STORE_ID não configuradas"
        }), 500
    return None


def merge_translations(current: dict, updates: dict) -> dict:
    merged = dict(current or {})
    for lang, value in (updates or {}).items():
        if value is not None and value != "":
            merged[lang] = value
    return merged


@app.route("/")
def home():
    return "App rodando"


@e("/produtos")
def listar_produtos():
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    url = f"{BASE_URL}/{store_id}/products"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)
    return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/produto/<int:produto_id>")
def get_produto(produto_id: int):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    url = f"{BASE_URL}/{store_id}/products/{produto_id}"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)
    return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/produto-revisao/<int:produto_id>")
def produto_revisao(produto_id: int):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    url = f"{BASE_URL}/{store_id}/products/{produto_id}"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)

    if response.status_code != 200:
        return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}

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


@app.route("/atualizar-produto-json/<int:produto_id>", methods=["POST"])
def atualizar_produto_json(produto_id: int):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/products/{produto_id}"

    get_response = requests.get(url, headers=headers, timeout=30)
    if get_response.status_code != 200:
        return get_response.text, get_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

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
    return put_response.text, put_response.status_code, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/categorias")
def listar_categorias():
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    url = f"{BASE_URL}/{store_id}/categories"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)
    return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/categoria/<int:categoria_id>")
def get_categoria(categoria_id: int):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    url = f"{BASE_URL}/{store_id}/categories/{categoria_id}"
    response = requests.get(url, headers=get_headers(access_token), timeout=30)
    return response.text, response.status_code, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/categoria-revisao/<int:categoria_id>")
def categoria_revisao(categoria_id: int):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

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


@app.route("/atualizar-categoria-json/<int:categoria_id>", methods=["POST"])
def atualizar_categoria_json(categoria_id: int):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/categories/{categoria_id}"

    get_response = requests.get(url, headers=headers, timeout=30)
    if get_response.status_code != 200:
        return get_response.text, get_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    categoria_atual = get_response.json()
    body = request.get_json(silent=True) or {}

    payload = {
        "name": merge_translations(categoria_atual.get("name", {}), body.get("name", {})),
        "description": merge_translations(categoria_atual.get("description", {}), body.get("description", {})),
        "handle": merge_translations(categoria_atual.get("handle", {}), body.get("handle", {})),
        "seo_title": merge_translations(categoria_atual.get("seo_title", {}), body.get("seo_title", {})),
        "seo_description": merge_translations(categoria_atual.get("seo_description", {}), body.get("seo_description", {})),
    }

    put_response = requests.put(url, headers=headers, json=payload, timeout=30)
    return put_response.text, put_response.status_code, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/preview-categoria-json/<int:categoria_id>", methods=["POST"])
def preview_categoria_json(categoria_id: int):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/categories/{categoria_id}"

    get_response = requests.get(url, headers=headers, timeout=30)
    if get_response.status_code != 200:
        return get_response.text, get_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    categoria_atual = get_response.json()
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
            "name": merge_translations(categoria_atual.get("name", {}), body.get("name", {})),
            "description": merge_translations(categoria_atual.get("description", {}), body.get("description", {})),
            "handle": merge_translations(categoria_atual.get("handle", {}), body.get("handle", {})),
            "seo_title": merge_translations(categoria_atual.get("seo_title", {}), body.get("seo_title", {})),
            "seo_description": merge_translations(categoria_atual.get("seo_description", {}), body.get("seo_description", {}))
        }
    }

    return jsonify(preview)


@app.route("/preview-produto-json/<int:produto_id>", methods=["POST"])
def preview_produto_json(produto_id: int):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return err

    headers = get_headers(access_token)
    url = f"{BASE_URL}/{store_id}/products/{produto_id}"

    get_response = requests.get(url, headers=headers, timeout=30)
    if get_response.status_code != 200:
        return get_response.text, get_response.status_code, {"Content-Type": "application/json; charset=utf-8"}

    produto_atual = get_response.json()
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
            "name": merge_translations(produto_atual.get("name", {}), body.get("name", {})),
            "description": merge_translations(produto_atual.get("description", {}), body.get("description", {})),
            "handle": merge_translations(produto_atual.get("handle", {}), body.get("handle", {})),
            "seo_title": merge_translations(produto_atual.get("seo_title", {}), body.get("seo_title", {})),
            "seo_description": merge_translations(produto_atual.get("seo_description", {}), body.get("seo_description", {}))
        }
    }

    return jsonify(preview)

# AUDITORIA BACKEND

def normalize_text(value):
    return (value or "").strip()


def get_lang_field(data: dict, field_name: str) -> dict:
    field = data.get(field_name, {}) or {}
    return {
        "pt": normalize_text(field.get("pt")),
        "en": normalize_text(field.get("en")),
        "es": normalize_text(field.get("es")),
    }


def analyze_translations(field: dict) -> dict:
    pt = normalize_text(field.get("pt"))
    en = normalize_text(field.get("en"))
    es = normalize_text(field.get("es"))

    values = {"pt": pt, "en": en, "es": es}
    non_empty_values = [v for v in values.values() if v]

    missing_languages = [lang for lang, value in values.items() if not value]

    all_equal_non_empty = (
        len(non_empty_values) == 3 and len(set(non_empty_values)) == 1
    )

    return {
        "missing_languages": missing_languages,
        "all_equal_non_empty": all_equal_non_empty,
        "en_equals_pt": bool(en and pt and en == pt),
        "es_equals_pt": bool(es and pt and es == pt),
        "has_issue": bool(missing_languages or all_equal_non_empty or (en and pt and en == pt) or (es and pt and es == pt))
    }


def fetch_all_items(resource: str):
    access_token, store_id = get_env_credentials()
    err = error_if_missing_credentials(access_token, store_id)
    if err:
        return None, err

    headers = get_headers(access_token)
    all_items = []
    page = 1

    while True:
        url = f"{BASE_URL}/{store_id}/{resource}"
        response = requests.get(
            url,
            headers=headers,
            params={"page": page, "per_page": 200},
            timeout=30
        )

        if response.status_code != 200:
            return None, (
                response.text,
                response.status_code,
                {"Content-Type": "application/json; charset=utf-8"}
            )

        items = response.json()

        if not items:
            break

        all_items.extend(items)
        page += 1

    return all_items, None

# AUDITORIA BACKEND
@app.route("/auditoria-seo-produtos", methods=["GET"])
def auditoria_seo_produtos():
    produtos, err = fetch_all_items("products")
    if err:
        return err

    produtos_auditados = []

    for p in produtos:
        handle = get_lang_field(p, "handle")
        seo_title = get_lang_field(p, "seo_title")
        seo_description = get_lang_field(p, "seo_description")

        flags_handle = analyze_translations(handle)
        flags_seo_title = analyze_translations(seo_title)
        flags_seo_description = analyze_translations(seo_description)

        has_issue = (
            flags_handle["has_issue"] or
            flags_seo_title["has_issue"] or
            flags_seo_description["has_issue"]
        )

        produtos_auditados.append({
            "id": p.get("id"),
            "name": get_lang_field(p, "name"),
            "handle": handle,
            "seo_title": seo_title,
            "seo_description": seo_description,
            "flags": {
                "handle": flags_handle,
                "seo_title": flags_seo_title,
                "seo_description": flags_seo_description,
                "has_issue": has_issue
            }
        })

    total_com_problema = sum(1 for item in produtos_auditados if item["flags"]["has_issue"])

    return jsonify({
        "resource": "products",
        "total": len(produtos_auditados),
        "total_com_problema": total_com_problema,
        "produtos": produtos_auditados
    })


@app.route("/auditoria-seo-categorias", methods=["GET"])
def auditoria_seo_categorias():
    categorias, err = fetch_all_items("categories")
    if err:
        return err

    categorias_auditadas = []

    for c in categorias:
        handle = get_lang_field(c, "handle")
        seo_title = get_lang_field(c, "seo_title")
        seo_description = get_lang_field(c, "seo_description")

        flags_handle = analyze_translations(handle)
        flags_seo_title = analyze_translations(seo_title)
        flags_seo_description = analyze_translations(seo_description)

        has_issue = (
            flags_handle["has_issue"] or
            flags_seo_title["has_issue"] or
            flags_seo_description["has_issue"]
        )

        categorias_auditadas.append({
            "id": c.get("id"),
            "name": get_lang_field(c, "name"),
            "handle": handle,
            "seo_title": seo_title,
            "seo_description": seo_description,
            "flags": {
                "handle": flags_handle,
                "seo_title": flags_seo_title,
                "seo_description": flags_seo_description,
                "has_issue": has_issue
            }
        })

    total_com_problema = sum(1 for item in categorias_auditadas if item["flags"]["has_issue"])

    return jsonify({
        "resource": "categories",
        "total": len(categorias_auditadas),
        "total_com_problema": total_com_problema,
        "categorias": categorias_auditadas
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
