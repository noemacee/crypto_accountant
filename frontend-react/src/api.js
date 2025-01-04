import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5001", // Flask backend URL
});

export const processWallet = (walletAddress, apiKey) =>
  api.post("/wallet/process_wallet", { wallet_address: walletAddress }, { headers: { "X-API-Key": apiKey } });

export const downloadCSV = (filePath) =>
  api.get("/download_csv", { params: { path: filePath }, responseType: "blob" });

export const login = (username, password) =>
  api.post("/login", { username, password });

export const register = (data) => api.post("/register", data);

export const getUsageStats = (apiKey) =>
  api.post("/usage_stats", {}, { headers: { "X-API-Key": apiKey } });

export const getAllUsageStats = () => api.get("/all_usage_stats");

export default api;
