import axios from "axios"

/**
 * Central Axios instance. Every API call goes through this client
 * (never raw fetch) so base URL, headers, and interceptors live in one place.
 */
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api"

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})
