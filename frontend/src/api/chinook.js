import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

export const getTracks = (params) => API.get("/tracks", { params });
export const getGenres = () => API.get("/genres");
export const getArtists = () => API.get("/artists");
export const getCustomers = () => API.get("/customers");
export const purchase = (body) => API.post("/purchase", body);


