import { apiClient } from "./client"
import type { User } from "@/types"

export interface ProfileUpdate {
  first_name?: string
  last_name?: string
  username?: string
  birthday?: string | null
  phone?: string
  preferences?: Record<string, unknown>
}

export async function updateProfile(patch: ProfileUpdate): Promise<User> {
  const { data } = await apiClient.patch<User>("/accounts/profile/", patch)
  return data
}

export async function uploadAvatar(image: Blob): Promise<string> {
  const form = new FormData()
  form.append("image", image, "avatar")
  const { data } = await apiClient.post<{ avatar_url: string }>(
    "/accounts/avatar/",
    form,
    { headers: { "Content-Type": "multipart/form-data" } },
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

export async function deactivateAccount(): Promise<void> {
  await apiClient.post("/accounts/deactivate/")
}

export async function deleteAccount(password?: string): Promise<void> {
  await apiClient.post("/accounts/delete/", password ? { password } : {})
}

export async function resetProgress(): Promise<void> {
  await apiClient.post("/accounts/reset-progress/")
}

export async function exportMyData(): Promise<Record<string, unknown>> {
  const { data } = await apiClient.get<Record<string, unknown>>(
    "/accounts/export/",
  )
  return data
}
