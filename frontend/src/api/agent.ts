import http from './request'
import type { AgentChatRequest, AgentChatResponse } from '@/types/agent'

export const sendAgentMessage = async (
  payload: AgentChatRequest,
): Promise<AgentChatResponse> => {
  return http.post<AgentChatResponse>('/agent/chat', payload)
}
