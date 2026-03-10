from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass
class RawListing:
    source: str
    source_url: str
    title: str
    description: str
    state: str | None
    city: str | None
    address: str | None
    category: str | None
    asking_price: float | None
    annual_revenue: float | None
    owner_name: str | None
    owner_phone: str | None
    owner_email: str | None
    legal_issues_summary: str | None
    development_notes: str | None
    latitude: float | None
    longitude: float | None


def _market_price_from_listing(asking_price: float | None, annual_revenue: float | None) -> float | None:
    if asking_price is None and annual_revenue is None:
        return None
    if asking_price is None:
        return round(annual_revenue * 0.75, 2)
    if annual_revenue is None:
        return round(asking_price * 0.98, 2)
    return round((asking_price * 0.65) + (annual_revenue * 0.35), 2)


def scrape_reddit_business_for_sale(limit: int = 20) -> Iterable[RawListing]:
    """Pull public Reddit posts from r/businessesforsale JSON feed."""
    import httpx

    url = "https://www.reddit.com/r/businessesforsale/new.json"
    headers = {"User-Agent": "business-sale-finder/0.1"}
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        response = client.get(url, params={"limit": limit}, headers=headers)
        response.raise_for_status()
        data = response.json()

    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        desc = post.get("selftext") or post.get("title", "")
        price = _extract_price(post.get("title", "") + " " + desc)
        yield RawListing(
            source="reddit",
            source_url=f"https://www.reddit.com{post.get('permalink', '')}",
            title=post.get("title", "Untitled post"),
            description=desc[:3500],
            state=None,
            city=None,
            address=None,
            category="unknown",
            asking_price=price,
            annual_revenue=None,
            owner_name=post.get("author"),
            owner_phone=None,
            owner_email=None,
            legal_issues_summary=None,
            development_notes="Captured from public subreddit post",
            latitude=None,
            longitude=None,
        )


def demo_seed_records() -> list[RawListing]:
    now_stamp = datetime.utcnow().strftime("%Y-%m-%d")
    return [
        RawListing(
            source="demo-public-record",
            source_url=f"https://example.com/listing/1?d={now_stamp}",
            title="HVAC service company for sale",
            description="Family-owned HVAC contractor with 15 technicians and recurring maintenance contracts.",
            state="TX",
            city="Austin",
            address="1200 Commerce St, Austin, TX",
            category="services",
            asking_price=1250000,
            annual_revenue=1800000,
            owner_name="Public filing only",
            owner_phone=None,
            owner_email=None,
            legal_issues_summary="No open district court cases found in last 24 months.",
            development_notes="2 major mixed-use developments filed within 5 miles.",
            latitude=30.2672,
            longitude=-97.7431,
        ),
        RawListing(
            source="demo-public-record",
            source_url=f"https://example.com/listing/2?d={now_stamp}",
            title="Branded coffee kiosk portfolio",
            description="Three profitable kiosks in high-footfall transit locations.",
            state="WA",
            city="Seattle",
            address="4th Ave, Seattle, WA",
            category="food",
            asking_price=550000,
            annual_revenue=720000,
            owner_name="Public filing only",
            owner_phone="(206) 555-0199",
            owner_email="seller@example.org",
            legal_issues_summary="One historical wage claim resolved in 2022.",
            development_notes="Transit station expansion should increase foot traffic.",
            latitude=47.6062,
            longitude=-122.3321,
        ),
        RawListing(
            source="demo-public-record",
            source_url=f"https://example.com/listing/3?d={now_stamp}",
            title="Neighborhood gas station with convenience store",
            description="Corner-lot fuel station with 4 pumps and a small C-store near commuter routes.",
            state="IL",
            city="Chicago",
            address="3100 S Halsted St, Chicago, IL",
            category="gas_station",
            asking_price=475000,
            annual_revenue=640000,
            owner_name="Public filing only",
            owner_phone="(312) 555-0117",
            owner_email="chicago.seller@example.org",
            legal_issues_summary="No open Cook County business-license enforcement actions found.",
            development_notes="Planned streetscape and transit corridor improvements within 2 miles.",
            latitude=41.8369,
            longitude=-87.6467,
        ),
    ]


def _extract_price(text: str) -> float | None:
    digits = []
    for token in text.replace(",", " ").replace("$", " $").split():
        if token.startswith("$") and token[1:].isdigit():
            digits.append(float(token[1:]))
    return max(digits) if digits else None


def estimate_market_price(raw: RawListing) -> float | None:
    return _market_price_from_listing(raw.asking_price, raw.annual_revenue)
