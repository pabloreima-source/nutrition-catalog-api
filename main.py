from fastapi import FastAPI, Query, Body
import requests

app = FastAPI()

# ---------------------------------------------------------
# ROOT (para comprobar que la API está viva)
# ---------------------------------------------------------

@app.get("/")
def root():
    return {"ok": True}


# ---------------------------------------------------------
# ENDPOINT INDIVIDUAL (1 alimento)
# ---------------------------------------------------------

@app.get("/catalog/verify_from_off")
def verify_from_off(q: str = Query(...), lang: str = "es"):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": q,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
        "fields": "product_name,nutriments,lang"
    }

    r = requests.get(url, params=params, timeout=15)
    data = r.json()

    for p in data.get("products", []):

