import { apiClient, TOKEN_KEY } from "./client"
import type { User } from "@/types"

interface TokenResponse {
  key?: string
}

export type SocialProvider = "google" | "github"

export interface OnboardingPayload {
  username: string
  password: string
  first_name: string
  last_name: string
  birthday?: string
  phone?: string
}

/** Exchange an OAuth `code` (from the provider callback) for a DRF token. */
export async function socialLogin(
  provider: SocialProvider,
  code: string,
): Promise<string> {
  const { data } = await apiClient.post<TokenResponse>(`/auth/${provider}/`, {
    code,
  })
  if (!data.key) throw new Error("Social login did not return a token")
  localStorage.setItem(TOKEN_KEY, data.key)
  return data.key
}

/** Username + password login (the password is set during onboarding). */
export async function loginUser(
  username: string,
  password: string,
): Promise<string> {
  const { data } = await apiClient.post<TokenResponse>("/auth/login/", {
    username,
    password,
  })
  if (!data.key) throw new Error("Login did not return a token")
  localStorage.setItem(TOKEN_KEY, data.key)
  return data.key
}

/** First-run profile setup after a social sign-in. */
export async function completeOnboarding(
  payload: OnboardingPayload,
): Promise<User> {
  const { data } = await apiClient.post<User>(
    "/accounts/complete-onboarding/",
    {
      username: payload.username,
      password: payload.password,
      first_name: payload.first_name,
      last_name: payload.last_name,
      birthday: payload.birthday || null,
      phone: payload.phone || "",
    },
  )
  return data
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
