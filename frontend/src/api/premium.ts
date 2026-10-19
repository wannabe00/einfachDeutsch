import { apiClient } from "./client"
import type { PremiumStatus } from "@/types"

/** Am I premium, is my trial still unused, and do I have a subscription? */
export async function fetchPremiumStatus(): Promise<PremiumStatus> {
  const { data } = await apiClient.get<PremiumStatus>("/accounts/premium/")
  return data
}

/** Stripe Checkout for a plan; resolves to the page to send the browser to. */
export async function startCheckout(plan: "monthly" | "annual"): Promise<string> {
  const { data } = await apiClient.post<{ url: string }>("/billing/checkout/", { plan })
  return data.url
}

/** The Stripe Customer Portal (cancel, change plan, card, invoices). */
export async function openPortal(): Promise<string> {
  const { data } = await apiClient.post<{ url: string }>("/billing/portal/")
  return data.url
}
