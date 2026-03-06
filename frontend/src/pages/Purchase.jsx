import { useState, useEffect } from "react";
import { getCustomers, purchase } from "../api/chinook";

export default function Purchase({ cart, setCart }) {
  const [customers, setCustomers] = useState([]);
  const [customerId, setCustomerId] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getCustomers().then((r) => setCustomers(r.data.customers));
  }, []);

  const total = cart.reduce((sum, t) => sum + t.UnitPrice, 0);

  const handlePurchase = async () => {
    if (!customerId) {
      alert("⚠️ Selecciona un cliente");
      return;
    }
    if (cart.length === 0) {
      alert("⚠️ El carrito está vacío");
      return;
    }

    setLoading(true);
    try {
      const res = await purchase({
        customer_id: parseInt(customerId),
        items: cart.map((t) => ({
          track_id: t.TrackId,
          unit_price: t.UnitPrice,
        })),
      });
      alert(`✅ Compra exitosa! Factura #${res.data.invoice_id} - Total: $${res.data.total.toFixed(2)}`);
      setCart([]);
      setCustomerId("");
    } catch (e) {
      alert("❌ Error al procesar la compra");
    } finally {
      setLoading(false);
    }
  };

  const removeFromCart = (trackId) => {
    setCart(cart.filter((t) => t.TrackId !== trackId));
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: "600px", margin: "0 auto" }}>
      <h1>🛒 Carrito de Compras</h1>

      {cart.length === 0 ? (
        <p style={{ color: "#888" }}>No hay canciones en el carrito.</p>
      ) : (
        <>
          {cart.map((t) => (
            <div key={t.TrackId} style={{
              display: "flex", justifyContent: "space-between",
              alignItems: "center", padding: "0.8rem",
              borderBottom: "1px solid #eee"
            }}>
              <div>
                <strong>{t.track_name}</strong>
                <p style={{ margin: 0, color: "#555", fontSize: "0.9rem" }}>{t.artist_name}</p>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
                <span style={{ color: "#1db954", fontWeight: "bold" }}>${t.UnitPrice}</span>
                <button onClick={() => removeFromCart(t.TrackId)} style={{
                  background: "#ff4444", color: "white",
                  border: "none", borderRadius: "6px",
                  padding: "0.3rem 0.7rem", cursor: "pointer"
                }}>✕</button>
              </div>
            </div>
          ))}

          <div style={{ marginTop: "1rem", fontSize: "1.2rem", fontWeight: "bold" }}>
            Total: ${total.toFixed(2)}
          </div>
        </>
      )}

      {/* Selector de cliente */}
      <div style={{ marginTop: "2rem" }}>
        <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: "bold" }}>
          Selecciona cliente:
        </label>
        <select
          value={customerId}
          onChange={(e) => setCustomerId(e.target.value)}
          style={{ padding: "0.5rem", borderRadius: "8px", width: "100%", fontSize: "1rem" }}
        >
          <option value="">-- Seleccionar --</option>
          {customers.map((c) => (
            <option key={c.CustomerId} value={c.CustomerId}>
              {c.FirstName} {c.LastName} ({c.Email})
            </option>
          ))}
        </select>
      </div>

      <button
        onClick={handlePurchase}
        disabled={loading}
        style={{
          marginTop: "1.5rem", width: "100%",
          padding: "0.8rem", borderRadius: "8px",
          background: loading ? "#ccc" : "#1db954",
          color: "white", border: "none",
          fontSize: "1.1rem", cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Procesando..." : "Confirmar Compra"}
      </button>
    </div>
  );
}


