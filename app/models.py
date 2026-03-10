from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    source_url: str = Field(index=True, unique=True)
    title: str
    description: str
    state: Optional[str] = Field(default=None, index=True)
    city: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = Field(default=None, index=True)
    asking_price: Optional[float] = None
    estimated_market_price: Optional[float] = None
    annual_revenue: Optional[float] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_email: Optional[str] = None
    legal_issues_summary: Optional[str] = None
    development_notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    last_seen: datetime = Field(default_factory=datetime.utcnow, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ListingSearch(SQLModel):
    q: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class RefreshResult(SQLModel):
    fetched: int
    inserted: int
    updated: int
