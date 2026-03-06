import { useState, useEffect } from "react";
import { getTracks, getGenres, getArtists } from "../api/chinook";
import TrackCard from "../components/TrackCard";

export default function Home({ cart, setCart }) {
  const [tracks, setTracks] = useState([]);
  const [genres, setGenres] = useState([]);
  const [artists, setArtists] = useState([]);
  const [filters, setFilters] = useState({ name: "", artist: "", genre: "" });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getGenres().then((r) => setGenres(r.data.genres));
    getArtists().then((r) => setArtists(r.data.artists));
    handleSearch();
  }, []);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const res = await getTracks(filters);
      setTracks(res.data.tracks);
    } catch (e) {
      alert("Error al cargar canciones");
    } finally {
      setLoading(false);
    }
  };

  const addToCart = (track) => {
    if (cart.find((t) => t.TrackId === track.TrackId)) {
      alert("Esta canción ya está en el carrito");
      return;
    }
    setCart([...cart, track]);
    alert(`✅ "${track.track_name}" agregada al carrito`);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>🎵 Chinook Music Store</h1>

      {/* Filtros */}
      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem", flexWrap: "wrap" }}>
        <input
          placeholder="Buscar canción..."
          value={filters.name}
          onChange={(e) => setFilters({ ...filters, name: e.target.value })}
          style={inputStyle}
        />
        <input
          placeholder="Buscar artista..."
          value={filters.artist}
          onChange={(e) => setFilters({ ...filters, artist: e.target.value })}
          style={inputStyle}
        />
        <select
          value={filters.genre}
          onChange={(e) => setFilters({ ...filters, genre: e.target.value })}
          style={inputStyle}
        >
          <option value="">Todos los géneros</option>
          {genres.map((g) => (
            <option key={g.GenreId} value={g.Name}>{g.Name}</option>
          ))}
        </select>
        <button onClick={handleSearch} style={btnStyle}>
          🔍 Buscar
        </button>
      </div>

      {/* Resultados */}
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "1rem" }}>
          {tracks.map((t) => (
            <TrackCard key={t.TrackId} track={t} onAdd={addToCart} />
          ))}
        </div>
      )}
    </div>
  );
}

const inputStyle = {
  padding: "0.5rem 1rem",
  borderRadius: "8px",
  border: "1px solid #ccc",
  fontSize: "1rem",
};

const btnStyle = {
  padding: "0.5rem 1.5rem",
  borderRadius: "8px",
  background: "#1db954",
  color: "white",
  border: "none",
  cursor: "pointer",
  fontSize: "1rem",
};

