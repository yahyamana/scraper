# Business for Sale Finder (MVP)

This repository includes a starter API + UI for finding businesses for sale and enriching leads with public-record style fields.

> ⚠️ Important: private contact details and scraping of protected sources may be regulated by local law and platform terms. Use public/authorized sources only.

## Features

- Unified listing model with state, city, address, category, asking price, market estimate, contact fields, legal/development notes, and coordinates.
- Source ingestion pipeline:
  - demo seed records
  - optional public Reddit `r/businessesforsale` JSON pull
- Search filters: keyword, state, category, min/max price.
- GeoJSON endpoint for map tooling.
- Browser UI at `/` to refresh data and run searches interactively.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

Open:
- UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## API examples

Refresh (without Reddit to avoid external dependency/rate limits):

```bash
curl -X POST "http://127.0.0.1:8000/refresh?include_reddit=false"
```

Find a gas station in Chicago under $500k:

```bash
curl "http://127.0.0.1:8000/listings?q=gas%20station&state=IL&category=gas_station&max_price=500000"
```

Map data:

```bash
curl "http://127.0.0.1:8000/map"
```
