import axios from 'axios'
import type { AxiosInstance } from 'axios'

const GATEWAY_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1'

const http: AxiosInstance = axios.create({
  baseURL: GATEWAY_BASE,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

http.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const detail = err.response?.data?.detail
    const message = detail || '请求失败，请重试'
    console.error('[API Error]', message)
    return Promise.reject(err)
  },
)

export default http
