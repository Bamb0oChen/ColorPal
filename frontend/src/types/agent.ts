export type AgentRole = 'user' | 'assistant'
export type AgentReplySource = 'model' | 'fallback'

export interface AgentMessage {
  id: string
  role: AgentRole
  content: string
  source?: AgentReplySource
}

export interface AgentChatHistoryItem {
  role: AgentRole
  content: string
}

export interface AgentChatRequest {
  message: string
  history: AgentChatHistoryItem[]
  user_id?: string
}

export interface AgentChatResponse {
  reply: string
  quick_replies: string[]
  source: AgentReplySource
}
