import http from './request'
import type { Post, Comment, CreatePostRequest, CreateCommentRequest } from '@/types/community'

export interface ApiResponse<T> {
  code: number
  data: T
  message: string
}

export const getPostList = async (): Promise<ApiResponse<Post[]>> => {
  return http.get('/community/posts')
}

export const getPostDetail = async (postId: string): Promise<ApiResponse<Post>> => {
  return http.get(`/community/posts/${postId}`)
}

export const createPost = async (data: CreatePostRequest): Promise<ApiResponse<Post>> => {
  const formData = new FormData()
  formData.append('content', data.content)
  if (data.images) {
    data.images.forEach((img) => formData.append('images', img))
  }
  if (data.photoRecordId) {
    formData.append('photoRecordId', data.photoRecordId)
  }
  return http.post('/community/posts', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const likePost = async (postId: string): Promise<ApiResponse<{ liked: boolean; likeCount: number }>> => {
  return http.post(`/community/posts/${postId}/like`)
}

export const getComments = async (postId: string): Promise<ApiResponse<Comment[]>> => {
  return http.get(`/community/posts/${postId}/comments`)
}

export const createComment = async (postId: string, data: CreateCommentRequest): Promise<ApiResponse<Comment>> => {
  return http.post(`/community/posts/${postId}/comments`, data)
}
