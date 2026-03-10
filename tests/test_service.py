from app.db import init_db, get_session
from app.models import ListingSearch
from app.service import refresh_sources, search_listings


def test_refresh_and_search_filters():
    init_db()
    with get_session() as session:
        result = refresh_sources(session, include_reddit=False)
        assert result.inserted >= 2

        tx = search_listings(session, ListingSearch(state="TX"))
        assert tx
        assert all(row.state == "TX" for row in tx)

        food = search_listings(session, ListingSearch(category="food"))
        assert food
        assert all(row.category == "food" for row in food)


def test_keyword_search_matches_description():
    init_db()
    with get_session() as session:
        refresh_sources(session, include_reddit=False)
        rows = search_listings(session, ListingSearch(q="technicians"))
        assert rows
        assert "HVAC" in rows[0].title


def test_find_chicago_gas_station_under_500k():
    init_db()
    with get_session() as session:
        refresh_sources(session, include_reddit=False)
        rows = search_listings(
            session,
            ListingSearch(q="gas station", state="IL", category="gas_station", max_price=500000),
        )
        assert rows
        assert rows[0].city == "Chicago"
        assert rows[0].asking_price <= 500000
