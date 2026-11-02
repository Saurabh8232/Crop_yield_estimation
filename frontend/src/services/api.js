import axios from "axios";

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL || "/api";
const apiBaseUrl = configuredBaseUrl === "/api"
  ? configuredBaseUrl
  : `${configuredBaseUrl.replace(/\/+$/, "")}/api`;

const api = axios.create({
  baseURL: apiBaseUrl,
  headers: { "Content-Type": "application/json" },
});

export const getHealth = () => api.get("/health");
export const getOptions = () => Promise.all([
  api.get("/crops"), api.get("/states"), api.get("/seasons"),
  api.get("/soil-types"), api.get("/years"),
]);
export const getDistricts = (state) => api.get("/districts", { params: state ? { state } : {} });
export const getAnalytics = () => api.get("/analytics");
export const getModelInfo = () => api.get("/model-info");
export const getHistory = () => api.get("/history");
export const predictYield = (payload) => api.post("/predict", payload);
