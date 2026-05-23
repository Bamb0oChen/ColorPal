import http from './request'
import type { DiscussionLoginStart, UserSession } from '@/types/auth'

export const startGithubDiscussionLogin = async (): Promise<DiscussionLoginStart> => {
  return http.get('/auth/github-discussion/start')
}

export const completeGithubDiscussionLogin = async (
  displayName: string,
  discussionUrl: string,
): Promise<UserSession> => {
  return http.post('/auth/github-discussion/login', {
    display_name: displayName,
    discussion_url: discussionUrl,
  })
}
