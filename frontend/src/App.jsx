import { useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import Purchase from "./pages/Purchase";

export default function App() {
  const [cart, setCart] = useState([]);

  return (
    <BrowserRouter>
      {/* Navbar */}
      <nav style={{
        background: "#191414", padding: "1rem 2rem",
        display: "flex", justifyContent: "space-between",
        alignItems: "center"
      }}>
        <Link to="/" style={{ color: "#1db954", fontWeight: "bold", fontSize: "1.3rem", textDecoration: "none" }}>
          🎵 Chinook
        </Link>
        <Link to="/purchase" style={{ color: "white", textDecoration: "none", fontSize: "1rem" }}>
          🛒 Carrito ({cart.length})
        </Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home cart={cart} setCart={setCart} />} />
        <Route path="/purchase" element={<Purchase cart={cart} setCart={setCart} />} />
      </Routes>
    </BrowserRouter>
  );
}

