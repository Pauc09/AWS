import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from app.main import app
from app.db.session import get_db


# ── HEALTH ───────────────────────────────────────────────
@pytest.mark.asyncio
async def test_health_db():
    """Verifica que el endpoint de salud responde ok"""
    async def override_get_db():
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 1
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health-db")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["ok"] == True


# ── TRACKS ───────────────────────────────────────────────
@pytest.mark.asyncio
async def test_get_tracks_returns_list():
    """Verifica que /tracks devuelve una lista de canciones"""
    async def override_get_db():
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = [
            {"TrackId": 1, "track_name": "Back In Black", "UnitPrice": 0.99,
             "artist_name": "AC/DC", "genre_name": "Rock", "album_title": "Back In Black"}
        ]
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tracks")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "tracks" in response.json()
    assert "count" in response.json()


@pytest.mark.asyncio
async def test_get_tracks_with_filters():
    """Verifica que los filtros de búsqueda funcionan"""
    async def override_get_db():
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tracks?name=Back&artist=AC/DC&genre=Rock")
    app.dependency_overrides.clear()

    assert response.status_code == 200


# ── GENRES ───────────────────────────────────────────────
@pytest.mark.asyncio
async def test_get_genres():
    """Verifica que /genres devuelve lista de géneros"""
    async def override_get_db():
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = [
            {"GenreId": 1, "Name": "Rock"},
            {"GenreId": 2, "Name": "Jazz"},
        ]
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/genres")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "genres" in response.json()


# ── ARTISTS ──────────────────────────────────────────────
@pytest.mark.asyncio
async def test_get_artists():
    """Verifica que /artists devuelve lista de artistas"""
    async def override_get_db():
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = [
            {"ArtistId": 1, "Name": "AC/DC"}
        ]
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/artists")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "artists" in response.json()


# ── CUSTOMERS ────────────────────────────────────────────
@pytest.mark.asyncio
async def test_get_customers():
    """Verifica que /customers devuelve lista de clientes"""
    async def override_get_db():
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = [
            {"CustomerId": 1, "FirstName": "John", "LastName": "Doe",
             "Email": "john@email.com", "Country": "USA"}
        ]
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/customers")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "customers" in response.json()


# ── PURCHASE ─────────────────────────────────────────────
@pytest.mark.asyncio
async def test_purchase_empty_cart():
    """Verifica que comprar con carrito vacío da error 400"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/purchase", json={
            "customer_id": 1,
            "items": []
        })

    assert response.status_code == 400
    assert "No items" in response.json()["detail"]


@pytest.mark.asyncio
async def test_purchase_success():
    """Verifica que una compra válida devuelve invoice_id"""
    async def override_get_db():
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = 42
        mock_session.execute.return_value = mock_result
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/purchase", json={
            "customer_id": 1,
            "items": [{"track_id": 1, "unit_price": 0.99}]
        })
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert "invoice_id" in response.json()
    assert "total" in response.json()

