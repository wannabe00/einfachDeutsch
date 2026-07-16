import { apiClient } from "./client"
import type { Conversation, ConversationDetail, ConversationMessage } from "@/types"

/* ChatGPT-style AI chat history (Phase 23.13). Premium-gated server-side. */

export async function fetchConversations(): Promise<Conversation[]> {
  const { data } = await apiClient.get<Conversation[]>("/ai/conversations/")
  return data
}

export async function fetchConversation(id: number): Promise<ConversationDetail> {
  const { data } = await apiClient.get<ConversationDetail>(`/ai/conversations/${id}/`)
  return data
}

export async function createConversation(): Promise<ConversationDetail> {
  const { data } = await apiClient.post<ConversationDetail>("/ai/conversations/")
  return data
}

export async function renameConversation(id: number, title: string): Promise<ConversationDetail> {
  const { data } = await apiClient.patch<ConversationDetail>(`/ai/conversations/${id}/`, { title })
  return data
}

export async function deleteConversation(id: number): Promise<void> {
  await apiClient.delete(`/ai/conversations/${id}/`)
}

/** Send a turn. Returns the persisted user + assistant messages. */
export async function sendMessage(
  id: number,
  message: string,
): Promise<{ conversation: Conversation; messages: ConversationMessage[] }> {
  const { data } = await apiClient.post<{
    conversation: Conversation
    messages: ConversationMessage[]
  }>(`/ai/conversations/${id}/messages/`, { message })
  return data
}
