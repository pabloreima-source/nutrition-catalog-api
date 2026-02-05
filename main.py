from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"ok": True}

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
        if p.get("lang") == lang:
            n = p.get("nutriments", {})
            return {
                "name": p.get("product_name"),
                "kcal_100g": n.get("energy-kcal_100g"),
                "protein_100g": n.get("proteins_100g"),
                "carbs_100g": n.get("carbohydrates_100g"),
                "fat_100g": n.get("fat_100g"),
                "source": "openfoodfacts"
            }

    return {"error": "not found"}
