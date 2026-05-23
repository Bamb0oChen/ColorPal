export interface User {
  id: string
  nickname: string
  avatar: string
}

export interface Post {
  id: string
  user: User
  content: string
  images: string[]
  photoRecord: {
    dominantColor: string
    palette: string[]
    score: number
  } | null
  likeCount: number
  commentCount: number
  liked: boolean
  createdAt: string
}

export interface Comment {
  id: string
  user: User
  content: string
  createdAt: string
}

export interface CreatePostRequest {
  content: string
  images?: File[]
  photoRecordId?: string
}

export interface CreateCommentRequest {
  content: string
}
