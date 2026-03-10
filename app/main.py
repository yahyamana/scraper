from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from .db import get_session, init_db
from .models import Listing, ListingSearch, RefreshResult
from .service import refresh_sources, search_listings

app = FastAPI(title="Business for Sale Finder", version="0.2.0")
UI_PATH = Path(__file__).parent / "ui" / "index.html"


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return UI_PATH.read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/refresh", response_model=RefreshResult)
def refresh(
    session: Annotated[Session, Depends(get_session)],
    include_reddit: bool = Query(default=True),
) -> RefreshResult:
    return refresh_sources(session, include_reddit=include_reddit)


@app.get("/listings", response_model=list[Listing])
def listings(
    session: Annotated[Session, Depends(get_session)],
    q: str | None = Query(default=None),
    state: str | None = Query(default=None),
    category: str | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None),
) -> list[Listing]:
    return search_listings(
        session,
        ListingSearch(q=q, state=state, category=category, min_price=min_price, max_price=max_price),
    )


@app.get("/listings/{listing_id}", response_model=Listing)
def listing_by_id(listing_id: int, session: Annotated[Session, Depends(get_session)]) -> Listing:
    item = session.exec(select(Listing).where(Listing.id == listing_id)).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return item


@app.get("/map")
def map_points(session: Annotated[Session, Depends(get_session)]) -> dict:
    points = []
    for row in session.exec(select(Listing).where(Listing.latitude.is_not(None), Listing.longitude.is_not(None))).all():
        points.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [row.longitude, row.latitude]},
                "properties": {
                    "id": row.id,
                    "title": row.title,
                    "price": row.asking_price,
                    "market_price": row.estimated_market_price,
                    "address": row.address,
                    "source": row.source,
                },
            }
        )

    return {"type": "FeatureCollection", "features": points}
