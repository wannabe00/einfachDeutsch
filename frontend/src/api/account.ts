import { apiClient } from "./client"
import type { User } from "@/types"

export interface ProfileUpdate {
  first_name?: string
  last_name?: string
  username?: string
  birthday?: string | null
  preferences?: Record<string, unknown>
}

export async function updateProfile(patch: ProfileUpdate): Promise<User> {
  const { data } = await apiClient.patch<User>("/accounts/profile/", patch)
  return data
}

export async function uploadAvatar(image: Blob): Promise<string> {
  const form = new FormData()
  form.append("image", image, "avatar")
  // Leave Content-Type unset so the browser adds the multipart boundary
  // (hardcoding "multipart/form-data" omits the boundary and the server
  // can't parse the upload). `undefined` clears the client's JSON default.
  const { data } = await apiClient.post<{ avatar_url: string }>(
    "/accounts/avatar/",
    form,
    { headers: { "Content-Type": undefined } },
  )
  return data.avatar_url
}

export async function changePassword(
  oldPassword: string,
  newPassword: string,
): Promise<void> {
  await apiClient.post("/auth/password/change/", {
    old_password: oldPassword,
    new_password1: newPassword,
    new_password2: newPassword,
  })
}

export async function logoutAllDevices(): Promise<void> {
  await apiClient.post("/accounts/logout-all/")
}

// Destructive actions require the account password server-side (AUDIT S2).
export async function deactivateAccount(password: string): Promise<void> {
  await apiClient.post("/accounts/deactivate/", { password })
}

export async function deleteAccount(password: string): Promise<void> {
  await apiClient.post("/accounts/delete/", { password })
}

export async function resetProgress(password: string): Promise<void> {
  await apiClient.post("/accounts/reset-progress/", { password })
}

export async function exportMyData(): Promise<Record<string, unknown>> {
  const { data } = await apiClient.get<Record<string, unknown>>(
    "/accounts/export/",
  )
  return data
}
