import http from './request'
import type { PhotoAnalyzeData } from '@/types/photo'

export const uploadAndAnalyze = async (
  file: File,
  location?: { lat: number; lng: number },
): Promise<PhotoAnalyzeData> => {
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
