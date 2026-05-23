import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getPostList, getPostDetail, createPost, likePost, getComments, createComment } from '@/api/community'
import type { Post, Comment } from '@/types/community'

export const useCommunityStore = defineStore('community', () => {
  const posts = ref<Post[]>([])
  const currentPost = ref<Post | null>(null)
  const comments = ref<Comment[]>([])
  const isLoading = ref(false)

  const fetchPosts = async () => {
    isLoading.value = true
    try {
      const res = await getPostList()
      posts.value = res.data
    } finally {
      isLoading.value = false
    }
  }

  const fetchPostDetail = async (postId: string) => {
    isLoading.value = true
    try {
      const res = await getPostDetail(postId)
      currentPost.value = res.data
    } finally {
      isLoading.value = false
    }
  }

  const fetchComments = async (postId: string) => {
    try {
      const res = await getComments(postId)
      comments.value = res.data
    } catch (err) {
      console.error('获取评论失败', err)
    }
  }

  const addPost = async (data: { content: string; images?: File[]; photoRecordId?: string }) => {
    const res = await createPost(data)
    posts.value.unshift(res.data)
    return res.data
  }

  const toggleLike = async (postId: string) => {
    const res = await likePost(postId)
    const post = posts.value.find(p => p.id === postId)
    if (post) {
      post.liked = res.data.liked
      post.likeCount = res.data.likeCount
    }
    if (currentPost.value && currentPost.value.id === postId) {
      currentPost.value.liked = res.data.liked
      currentPost.value.likeCount = res.data.likeCount
    }
  }

  const addComment = async (postId: string, content: string) => {
    const res = await createComment(postId, { content })
    comments.value.push(res.data)
    if (currentPost.value && currentPost.value.id === postId) {
      currentPost.value.commentCount += 1
    }
    const post = posts.value.find(p => p.id === postId)
    if (post) {
      post.commentCount += 1
    }
    return res.data
  }

  return {
    posts,
    currentPost,
    comments,
    isLoading,
    fetchPosts,
    fetchPostDetail,
    fetchComments,
    addPost,
    toggleLike,
    addComment
  }
})
