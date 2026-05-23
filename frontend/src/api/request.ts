import axios from 'axios'
import type { AxiosRequestConfig, AxiosResponse } from 'axios'

interface ApiEnvelope<T> {
  code: number
  data: T
  message: string
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const client = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  timeout: 15000,
})

const unwrap = <T>(response: AxiosResponse<ApiEnvelope<T> | T>): T => {
  const body = response.data
  if (body && typeof body === 'object' && 'code' in body && 'data' in body) {
    return (body as ApiEnvelope<T>).data
  }
  return body as T
}

client.interceptors.response.use(
  (res) => res,
  (err) => {
    const message = err.response?.data?.detail || '请求失败，请重试'
    console.error('[API Error]', message)
    return Promise.reject(err)
  },
)

const http = {
  get: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await client.get<ApiEnvelope<T> | T>(url, config)
    return unwrap<T>(response)
  },
  post: async <T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> => {
    const response = await client.post<ApiEnvelope<T> | T>(url, data, config)
    return unwrap<T>(response)
  },
}

export default http
