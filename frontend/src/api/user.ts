import http from './request'

export interface UserProfile {
  nickname: string
  avatar: string
  pet: {
    name: string
    stage: number
    mood: 'happy' | 'neutral' | 'sad'
    color: string
    energy: {
      current: number
      max: number
      r: number
      g: number
      b: number
    }
  }
  stats: {
    total_photos: number
    highest_score: number
    streak_days: number
  }
}

export const getProfile = async (): Promise<UserProfile> => {
  return http.get<UserProfile>('/user/profile')
}
