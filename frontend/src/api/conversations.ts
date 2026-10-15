import { apiClient } from "./client"
import type { ChatMode, Conversation, ConversationDetail, ConversationMessage } from "@/types"

/* Saved AI conversations. Premium only; the server enforces it. */

/** Pinned first, then most recent. `query` searches titles and messages. */
export async function fetchConversations(query = ""): Promise<Conversation[]> {
  const { data } = await apiClient.get<Conversation[]>("/ai/conversations/", {
    params: query ? { q: query } : undefined,
  })
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

export async function setPinned(id: number, pinned: boolean): Promise<ConversationDetail> {
  const { data } = await apiClient.patch<ConversationDetail>(`/ai/conversations/${id}/`, { pinned })
  return data
}

/** Answer the last message again; returns the replaced assistant message. */
export async function retryLastAnswer(id: number): Promise<ConversationMessage> {
  const { data } = await apiClient.post<ConversationMessage>(`/ai/conversations/${id}/retry/`)
  return data
}

export async function deleteConversation(id: number): Promise<void> {
  await apiClient.delete(`/ai/conversations/${id}/`)
}

/** Send a turn. Returns the persisted user + assistant messages. */
export async function sendMessage(
  id: number,
  message: string,
  mode: ChatMode,
): Promise<{ conversation: Conversation; messages: ConversationMessage[] }> {
  const { data } = await apiClient.post<{
    conversation: Conversation
    messages: ConversationMessage[]
  }>(`/ai/conversations/${id}/messages/`, { message, mode })
  return data
}
