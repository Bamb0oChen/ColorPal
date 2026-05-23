export interface DiscussionLoginStart {
  provider: 'github_discussions'
  discussion_url: string
  is_reachable: boolean
}

export interface UserSession {
  user_id: string
  display_name: string
  provider: 'github_discussions'
  discussion_url: string
  created_at: string
}
