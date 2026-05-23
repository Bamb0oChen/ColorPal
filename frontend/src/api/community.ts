import http from './request'
import type { Post, Comment } from '@/types/community'

function userHeaders() {
  const raw = localStorage.getItem('colorpal.session')
  if (!raw) return {}
  try {
    const session = JSON.parse(raw)
    return {
      'X-User-Id': session.user_id || 'user_001',
      'X-User-Name': session.display_name || '玩家',
    }
  } catch {
    return {}
  }
}

export const getPostList = async (): Promise<Post[]> => {
  return http.get('/community/posts', { headers: userHeaders() })
}

export const getPostDetail = async (postId: string): Promise<Post> => {
  return http.get(`/community/posts/${postId}`, { headers: userHeaders() })
}

export const createPost = async (data: { content: string; images?: File[] }): Promise<Post> => {
  const formData = new FormData()
  formData.append('content', data.content || '')
  if (data.images) {
    data.images.forEach((img) => formData.append('images', img))
  }
  return http.post('/community/posts', formData, {
    headers: userHeaders(),
  })
}

export const likePost = async (postId: string): Promise<{ liked: boolean; likeCount: number }> => {
  return http.post(`/community/posts/${postId}/like`, {}, { headers: userHeaders() })
}

export const getComments = async (postId: string): Promise<Comment[]> => {
  return http.get(`/community/posts/${postId}/comments`, { headers: userHeaders() })
}

export const createComment = async (postId: string, content: string): Promise<Comment> => {
  return http.post(`/community/posts/${postId}/comments`, { content }, { headers: userHeaders() })
}

export const getMyPosts = async (): Promise<Post[]> => {
  return http.get('/community/posts/mine', { headers: userHeaders() })
}

export const injectDevPosts = async (): Promise<Post[]> => {
  return http.post('/community/dev/inject', {}, { headers: userHeaders() })
}
