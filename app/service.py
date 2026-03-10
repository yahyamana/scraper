from __future__ import annotations

from datetime import datetime

from sqlmodel import Session, or_, select

from .models import Listing, ListingSearch, RefreshResult
from .sources import RawListing, demo_seed_records, estimate_market_price, scrape_reddit_business_for_sale


def upsert_listing(session: Session, raw: RawListing) -> tuple[bool, Listing]:
    existing = session.exec(select(Listing).where(Listing.source_url == raw.source_url)).first()
    if existing:
        existing.last_seen = datetime.utcnow()
        existing.title = raw.title
        existing.description = raw.description
        existing.asking_price = raw.asking_price
        existing.estimated_market_price = estimate_market_price(raw)
        existing.state = raw.state
        existing.city = raw.city
        existing.address = raw.address
        existing.category = raw.category
        existing.annual_revenue = raw.annual_revenue
        existing.owner_name = raw.owner_name
        existing.owner_phone = raw.owner_phone
        existing.owner_email = raw.owner_email
        existing.legal_issues_summary = raw.legal_issues_summary
        existing.development_notes = raw.development_notes
        existing.latitude = raw.latitude
        existing.longitude = raw.longitude
        session.add(existing)
        return False, existing

    listing = Listing(
        source=raw.source,
        source_url=raw.source_url,
        title=raw.title,
        description=raw.description,
        state=raw.state,
        city=raw.city,
        address=raw.address,
        category=raw.category,
        asking_price=raw.asking_price,
        estimated_market_price=estimate_market_price(raw),
        annual_revenue=raw.annual_revenue,
        owner_name=raw.owner_name,
        owner_phone=raw.owner_phone,
        owner_email=raw.owner_email,
        legal_issues_summary=raw.legal_issues_summary,
        development_notes=raw.development_notes,
        latitude=raw.latitude,
        longitude=raw.longitude,
    )
    session.add(listing)
    return True, listing


def refresh_sources(session: Session, include_reddit: bool = True) -> RefreshResult:
    fetched = inserted = updated = 0

    rows = demo_seed_records()
    if include_reddit:
        try:
            rows.extend(list(scrape_reddit_business_for_sale()))
        except Exception:
            # Keep refresh resilient if a public feed is rate-limited.
            pass

    for raw in rows:
        fetched += 1
        created, _ = upsert_listing(session, raw)
        if created:
            inserted += 1
        else:
            updated += 1

    session.commit()
    return RefreshResult(fetched=fetched, inserted=inserted, updated=updated)


def search_listings(session: Session, query: ListingSearch) -> list[Listing]:
    statement = select(Listing)
    if query.state:
        statement = statement.where(Listing.state == query.state.upper())
    if query.category:
        statement = statement.where(Listing.category == query.category.lower())
    if query.min_price is not None:
        statement = statement.where(Listing.asking_price >= query.min_price)
    if query.max_price is not None:
        statement = statement.where(Listing.asking_price <= query.max_price)
    if query.q:
        q = f"%{query.q.lower()}%"
        statement = statement.where(
            or_(
                Listing.title.ilike(q),
                Listing.description.ilike(q),
                Listing.city.ilike(q),
                Listing.state.ilike(q),
            )
        )
    statement = statement.order_by(Listing.last_seen.desc())
    return list(session.exec(statement).all())
