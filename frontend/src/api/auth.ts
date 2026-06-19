import { apiClient, TOKEN_KEY } from "./client"
import type { User } from "@/types"

interface TokenResponse {
  key: string
}

export async function registerUser(
  email: string,
  password: string,
): Promise<string> {
  const { data } = await apiClient.post<TokenResponse>("/auth/registration/", {
    email,
    password1: password,
    password2: password,
  })
  localStorage.setItem(TOKEN_KEY, data.key)
  return data.key
}

export async function loginUser(
  email: string,
  password: string,
): Promise<string> {
  const { data } = await apiClient.post<TokenResponse>("/auth/login/", {
    email,
    password,
  })
  localStorage.setItem(TOKEN_KEY, data.key)
  return data.key
}

export async function fetchCurrentUser(): Promise<User> {
  const { data } = await apiClient.get<User>("/auth/user/")
  return data
}

export async function logoutUser(): Promise<void> {
  try {
    await apiClient.post("/auth/logout/")
  } finally {
    localStorage.removeItem(TOKEN_KEY)
  }
}
