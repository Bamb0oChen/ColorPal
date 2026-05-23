import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getPostList, getPostDetail, createPost, likePost, getComments, createComment, injectDevPosts } from '@/api/community'
import type { Post, Comment } from '@/types/community'

export const useCommunityStore = defineStore('community', () => {
  const posts = ref<Post[]>([])
  const currentPost = ref<Post | null>(null)
  const comments = ref<Comment[]>([])
  const isLoading = ref(false)

  const fetchPosts = async () => {
    isLoading.value = true
    try {
      posts.value = await getPostList()
    } finally {
      isLoading.value = false
    }
  }

  const fetchPostDetail = async (postId: string) => {
    isLoading.value = true
    try {
      currentPost.value = await getPostDetail(postId)
    } finally {
      isLoading.value = false
    }
  }

  const fetchComments = async (postId: string) => {
    try {
      comments.value = await getComments(postId)
    } catch (err) {
      console.error('获取评论失败', err)
    }
  }

  const addPost = async (data: { content: string; images?: File[] }) => {
    const post = await createPost(data)
    posts.value.unshift(post)
    return post
  }

  const toggleLike = async (postId: string) => {
    const res = await likePost(postId)
    const post = posts.value.find((p) => p.id === postId)
    if (post) {
      post.liked = res.liked
      post.likeCount = res.likeCount
    }
    if (currentPost.value && currentPost.value.id === postId) {
      currentPost.value.liked = res.liked
      currentPost.value.likeCount = res.likeCount
    }
  }

  const addComment = async (postId: string, content: string) => {
    const comment = await createComment(postId, content)
    comments.value.push(comment)
    if (currentPost.value && currentPost.value.id === postId) {
      currentPost.value.commentCount += 1
    }
    const post = posts.value.find((p) => p.id === postId)
    if (post) {
      post.commentCount += 1
    }
    return comment
  }

  const injectPosts = async () => {
    const injected = await injectDevPosts()
    posts.value = [...injected, ...posts.value]
    return injected
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
    addComment,
    injectPosts,
  }
})
