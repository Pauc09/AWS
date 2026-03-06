from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title="Chinook Music Store")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── HEALTH ──────────────────────────────────────────────
@app.get("/health-db")
async def health_db(db: AsyncSession = Depends(get_db)):
    r = await db.execute(text("SELECT 1"))
    return {"ok": True, "db": r.scalar_one()}

# ── TRACKS ──────────────────────────────────────────────
@app.get("/tracks")
async def get_tracks(
    name: Optional[str] = Query(None),
    artist: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    q = """
        SELECT t.TrackId, t.Name as track_name, t.UnitPrice,
               ar.Name as artist_name, g.Name as genre_name,
               al.Title as album_title
        FROM Track t
        JOIN Album al ON t.AlbumId = al.AlbumId
        JOIN Artist ar ON al.ArtistId = ar.ArtistId
        JOIN Genre g ON t.GenreId = g.GenreId
        WHERE 1=1
    """
    params = {}
    if name:
        q += " AND t.Name LIKE :name"
        params["name"] = f"%{name}%"
    if artist:
        q += " AND ar.Name LIKE :artist"
        params["artist"] = f"%{artist}%"
    if genre:
        q += " AND g.Name LIKE :genre"
        params["genre"] = f"%{genre}%"
    q += " LIMIT 50"

    res = await db.execute(text(q), params)
    rows = res.mappings().all()
    return {"count": len(rows), "tracks": rows}

# ── GENRES ──────────────────────────────────────────────
@app.get("/genres")
async def get_genres(db: AsyncSession = Depends(get_db)):
    res = await db.execute(text("SELECT GenreId, Name FROM Genre ORDER BY Name"))
    return {"genres": res.mappings().all()}

# ── ARTISTS ─────────────────────────────────────────────
@app.get("/artists")
async def get_artists(db: AsyncSession = Depends(get_db)):
    res = await db.execute(text("SELECT ArtistId, Name FROM Artist ORDER BY Name"))
    return {"artists": res.mappings().all()}

# ── CUSTOMERS ───────────────────────────────────────────
@app.get("/customers")
async def get_customers(db: AsyncSession = Depends(get_db)):
    res = await db.execute(text("""
        SELECT CustomerId, FirstName, LastName, Email, Country
        FROM Customer ORDER BY FirstName
    """))
    return {"customers": res.mappings().all()}

# ── PURCHASE ────────────────────────────────────────────
class PurchaseItem(BaseModel):
    track_id: int
    unit_price: float

class PurchaseRequest(BaseModel):
    customer_id: int
    items: list[PurchaseItem]

@app.post("/purchase")
async def purchase(body: PurchaseRequest, db: AsyncSession = Depends(get_db)):
    if not body.items:
        raise HTTPException(status_code=400, detail="No items in purchase")

    total = sum(i.unit_price for i in body.items)

    # Crear Invoice
    res = await db.execute(text("""
        INSERT INTO Invoice (CustomerId, InvoiceDate, BillingAddress, Total)
        SELECT CustomerId, :date, Address, :total
        FROM Customer WHERE CustomerId = :cid
    """), {"date": datetime.utcnow(), "total": total, "cid": body.customer_id})
    await db.flush()

    invoice_id_res = await db.execute(text("SELECT LAST_INSERT_ID()"))
    invoice_id = invoice_id_res.scalar_one()

    # Crear InvoiceLines
    for item in body.items:
        await db.execute(text("""
            INSERT INTO InvoiceLine (InvoiceId, TrackId, UnitPrice, Quantity)
            VALUES (:inv_id, :track_id, :price, 1)
        """), {"inv_id": invoice_id, "track_id": item.track_id, "price": item.unit_price})

    await db.commit()
    return {"ok": True, "invoice_id": invoice_id, "total": total}