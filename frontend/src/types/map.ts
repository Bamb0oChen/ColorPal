export interface Location {
  lat: number
  lng: number
}

export interface Place {
  id: string
  name: string
  address: string
  location: Location
  category: string
  rating: number
  description: string
  image: string
  distance: number
  duration?: string
}

export interface RecommendRequest {
  query: string
  location?: Location
}

export interface RecommendResponse {
  places: Place[]
  centerLocation: Location
}
