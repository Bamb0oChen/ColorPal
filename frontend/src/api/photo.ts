import http from './request'

export interface UploadResponse {
  photo_id: string
  analysis: {
    dominant_color: string
    palette: string[]
    score: number
    comment: string
    color_category: string
    saturation_level: string
    brightness_level: string
  }
  energy_change: {
    r: number
    g: number
    b: number
    total: number
  }
  task_completed: string | null
}

export const uploadAndAnalyze = async (
  file: File,
  location?: { lat: number; lng: number },
): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('image', file)
  if (location) {
    formData.append('lat', String(location.lat))
    formData.append('lng', String(location.lng))
  }

  return http.post('/photo/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
