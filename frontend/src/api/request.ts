import axios from 'axios'
import type { AxiosInstance } from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const http: AxiosInstance = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  timeout: 15000,
})

http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const message = err.response?.data?.detail || '请求失败，请重试'
    console.error('[API Error]', message)
    return Promise.reject(new Error(message))
  },
)

export default http
