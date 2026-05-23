import http from './request'

export interface Place {
  id: string
  name: string
  address: string
  location: { lat: number; lng: number }
  category: string
  rating: number
  description: string
  image: string
  distance: number
  duration?: string
}

export interface RecommendResponse {
  places: Place[]
  centerLocation: { lat: number; lng: number }
}

export const getRecommendations = async (
  query: string,
  location?: { lat: number; lng: number },
): Promise<RecommendResponse> => {
  return http.post('/map/recommend', { query, location })
}

export const getLocation = async (): Promise<{ lat: number; lng: number; address: string }> => {
  return http.get('/map/location')
}
