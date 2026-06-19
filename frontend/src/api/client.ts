import axios from "axios"

/**
 * Central Axios instance. Every API call goes through this client
 * (never raw fetch) so base URL, headers, and interceptors live in one place.
 */
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api"

export const TOKEN_KEY = "auth_token"

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// Attach the auth token (DRF: "Authorization: Token <key>") to every request.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) config.headers.Authorization = `Token ${token}`
  return config
})

// On 401, clear the stale token and signal the app shell to bounce to login
// (a custom event keeps this module free of React/router imports).
apiClient.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401 && localStorage.getItem(TOKEN_KEY)) {
      localStorage.removeItem(TOKEN_KEY)
      window.dispatchEvent(new Event("auth:logout"))
    }
    return Promise.reject(error)
  },
)
