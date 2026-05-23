import http from './request'
import type { RecommendRequest, RecommendResponse } from '@/types/map'

export const getRecommendations = async (
  query: string,
  location?: { lat: number; lng: number },
): Promise<RecommendResponse> => {
  return http.post('/map/recommend', {
    query,
    location,
  })
}

export const getLocation = async (): Promise<{ lat: number; lng: number; address: string }> => {
  return http.get('/map/location')
}
