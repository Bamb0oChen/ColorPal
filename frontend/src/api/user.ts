import http from './request'

export interface UserProfile {
  nickname: string
  avatar: string
  pet: {
    name: string
    stage: number
    mood: 'happy' | 'neutral' | 'sad'
    color: string
    totalEnergy: number
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

export const updateEnergy = async (energy: {
  r: number
  g: number
  b: number
  total: number
}): Promise<{ energy: { current: number; max: number; r: number; g: number; b: number }; totalEnergy: number }> => {
  return http.post('/user/energy', energy)
}
