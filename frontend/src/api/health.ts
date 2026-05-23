import http from './request'

export interface HealthResponse {
  status: string
  service: string
}

export const checkHealth = async (): Promise<HealthResponse> => {
  return http.get('/health')
}
