export default function TrackCard({ track, onAdd }) {
  return (
    <div style={{
      border: "1px solid #ddd",
      borderRadius: "12px",
      padding: "1rem",
      background: "#fff",
      boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    }}>
      <h3 style={{ margin: "0 0 0.5rem" }}>{track.track_name}</h3>
      <p style={{ margin: "0.2rem 0", color: "#555" }}>🎤 {track.artist_name}</p>
      <p style={{ margin: "0.2rem 0", color: "#555" }}>💿 {track.album_title}</p>
      <p style={{ margin: "0.2rem 0", color: "#888" }}>🎸 {track.genre_name}</p>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "1rem" }}>
        <span style={{ fontWeight: "bold", color: "#1db954" }}>${track.UnitPrice}</span>
        <button onClick={() => onAdd(track)} style={{
          padding: "0.4rem 1rem",
          borderRadius: "8px",
          background: "#1db954",
          color: "white",
          border: "none",
          cursor: "pointer"
        }}>
          + Agregar
        </button>
      </div>
    </div>
  );
}

