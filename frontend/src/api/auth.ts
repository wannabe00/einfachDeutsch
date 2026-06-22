import { apiClient, TOKEN_KEY } from "./client"
import type { User } from "@/types"

interface TokenResponse {
  key?: string
}

export type RegisterResult =
  | { status: "logged_in" }
  | { status: "verify_email" }

export interface RegisterPayload {
  email: string
  password: string
  username: string
  first_name: string
  last_name: string
  birthday?: string
  phone?: string
}

export async function registerUser(
  payload: RegisterPayload,
): Promise<RegisterResult> {
  const { data } = await apiClient.post<TokenResponse>("/auth/registration/", {
    email: payload.email,
    password1: payload.password,
    password2: payload.password,
    username: payload.username,
    first_name: payload.first_name,
    last_name: payload.last_name,
    birthday: payload.birthday || null,
    phone: payload.phone || "",
  })
  // With mandatory email verification the backend returns no token — the user
  // must confirm their email before logging in. Without verification it would
  // return a token and we'd be logged in immediately.
  if (data.key) {
    localStorage.setItem(TOKEN_KEY, data.key)
    return { status: "logged_in" }
  }
  return { status: "verify_email" }
}

export async function verifyEmail(key: string): Promise<void> {
  await apiClient.post("/auth/registration/verify-email/", { key })
}

export async function loginUser(
  email: string,
  password: string,
): Promise<string> {
  const { data } = await apiClient.post<TokenResponse>("/auth/login/", {
    email,
    password,
  })
  if (!data.key) throw new Error("Login did not return a token")
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
