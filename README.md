# Google SERP export (JSON)

Jednoduchá webová aplikace pro zadání klíčového slovního spojení a získání organických výsledků z 1. stránky Google ve strukturovaném formátu **JSON**. Součástí je **unit test** (pytest).

## Funkce
- HTML stránka s jedním inputem
- vyhledání přes endpoint `/api/search?q=...`
- zobrazení 10 výsledků
- stažení výsledků jako `.json` soubor (ne HTML)

## Struktura projektu
- `public/` – frontend (`index.html`)
- `api/` – Flask API (`index.py`)
- `tests/` – unit testy (`test_api.py`)

## Požadavky
- Python 3.10+ (doporučeno)

## Lokální spuštění

1. Nainstaluj závislosti:
```bash
pip install -r requirements.txt

Nastav SerpAPI klíč:

Linux/macOS:
export SERPAPI_KEY="YOUR_KEY"

Windows PowerShell:
$env:SERPAPI_KEY="YOUR_KEY"

Spusť aplikaci:
python api/index.py

Otevři:

UI: http://127.0.0.1:8000/

API: http://127.0.0.1:8000/api/search?q=python

Testy
python -m pytest -q

Nasazení
Aplikace je připravená pro hosting (Render/Railway) přes gunicorn:
gunicorn api.index:app --bind 0.0.0.0:$PORT

Env proměnná na hostingu:
SERPAPI_KEY




