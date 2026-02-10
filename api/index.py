import os
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

SERPAPI_ENDPOINT = "https://serpapi.com/search.json"

# Absolute path to /public (one level above /api)
PUBLIC_DIR = (Path(__file__).resolve().parent.parent / "public").resolve()


def normalize_serpapi_response(data: dict, fallback_query: str | None = None) -> dict:
    organic = data.get("organic_results") or []
    results = []

    for i, item in enumerate(organic, start=1):
        results.append({
            "position": i,
            "title": item.get("title"),
            "link": item.get("link"),
            "displayLink": (item.get("displayed_link") or item.get("source")),
            "snippet": item.get("snippet"),
        })

    sp = data.get("search_parameters") or {}
    q = sp.get("q") or fallback_query

    return {"query": q, "count": len(results), "results": results}


@app.get("/")
def home():
    return send_from_directory(PUBLIC_DIR, "index.html")


@app.get("/<path:path>")
def static_files(path: str):
    return send_from_directory(PUBLIC_DIR, path)


@app.get("/api/search")
def search():
    serpapi_key = os.environ.get("SERPAPI_KEY")

    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    if not serpapi_key:
        return jsonify({"error": "Server is not configured (missing SERPAPI_KEY)"}), 500

    params = {
        "engine": "google",
        "q": q,
        "api_key": serpapi_key,
        "num": 10,   # 1st page (up to 10)
        "hl": "cs",  # language
        "gl": "cz",  # country
    }

    try:
        r = requests.get(SERPAPI_ENDPOINT, params=params, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": "Upstream request failed", "details": str(e)}), 502

    return jsonify(normalize_serpapi_response(r.json(), fallback_query=q)), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
