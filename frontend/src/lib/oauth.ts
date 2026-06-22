import type { SocialProvider } from "@/api/auth"

/**
 * Build the provider authorize URL and redirect the browser to it. The provider
 * sends the user back to `${origin}/auth/callback/<provider>?code=...`, where
 * OAuthCallbackPage posts the code to the backend for a token.
 *
 * Client IDs are public (safe in the frontend); the secrets live only on the
 * backend. The redirect URI must exactly match what's registered in the
 * Google Cloud / GitHub OAuth app.
 */
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID as string | undefined
const GITHUB_CLIENT_ID = import.meta.env.VITE_GITHUB_CLIENT_ID as string | undefined

export function isProviderConfigured(provider: SocialProvider): boolean {
  return provider === "google" ? !!GOOGLE_CLIENT_ID : !!GITHUB_CLIENT_ID
}

export function redirectUri(provider: SocialProvider): string {
  return `${window.location.origin}/auth/callback/${provider}`
}

export function startOAuth(provider: SocialProvider): void {
  // Random state for CSRF protection; verified on the callback.
  const state = crypto.randomUUID()
  sessionStorage.setItem(`oauth_state_${provider}`, state)

  const redirect = redirectUri(provider)
  let url: string

  if (provider === "google") {
    const params = new URLSearchParams({
      client_id: GOOGLE_CLIENT_ID ?? "",
      redirect_uri: redirect,
      response_type: "code",
      scope: "openid email profile",
      access_type: "online",
      prompt: "select_account",
      state,
    })
    url = `https://accounts.google.com/o/oauth2/v2/auth?${params}`
  } else {
    const params = new URLSearchParams({
      client_id: GITHUB_CLIENT_ID ?? "",
      redirect_uri: redirect,
      scope: "read:user user:email",
      state,
    })
    url = `https://github.com/login/oauth/authorize?${params}`
  }

  window.location.href = url
}

/** Validate the state returned on the callback against what we stored. */
export function consumeState(provider: SocialProvider, state: string | null): boolean {
  const expected = sessionStorage.getItem(`oauth_state_${provider}`)
  sessionStorage.removeItem(`oauth_state_${provider}`)
  return !!state && !!expected && state === expected
}
