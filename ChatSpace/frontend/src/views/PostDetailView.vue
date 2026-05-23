<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import PostCard from '@/components/community/PostCard.vue'
import CommentItem from '@/components/community/CommentItem.vue'

const router = useRouter()
const route = useRoute()
const communityStore = useCommunityStore()

const commentInput = ref('')
const isSubmitting = ref(false)

onMounted(async () => {
  const postId = route.params.id as string
  await Promise.all([
    communityStore.fetchPostDetail(postId),
    communityStore.fetchComments(postId)
  ])
})

const handleSubmitComment = async () => {
  if (!commentInput.value.trim()) return

  isSubmitting.value = true
  try {
    await communityStore.addComment(route.params.id as string, commentInput.value)
    commentInput.value = ''
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="post-detail-page">
    <header class="header">
      <button class="back-btn" @click="router.back()">返回</button>
      <h1>动态详情</h1>
      <div class="placeholder"></div>
    </header>

    <div v-if="communityStore.isLoading" class="loading">加载中...</div>
    <div v-else-if="!communityStore.currentPost" class="empty">动态不存在</div>
    <div v-else class="content">
      <PostCard
        :post="communityStore.currentPost"
        :show-actions="false"
        @like="communityStore.toggleLike"
      />

      <div class="comments-section">
        <div class="section-title">
          评论 ({{ communityStore.currentPost.commentCount }})
        </div>
        <div class="comments-list">
          <CommentItem
            v-for="comment in communityStore.comments"
            :key="comment.id"
            :comment="comment"
          />
          <div v-if="communityStore.comments.length === 0" class="no-comments">
            暂无评论，快来抢沙发！
          </div>
        </div>
      </div>
    </div>

    <div class="comment-input-wrapper">
      <input
        v-model="commentInput"
        class="comment-input"
        placeholder="说点什么..."
        @keyup.enter="handleSubmitComment"
      />
      <button
        class="send-btn"
        :disabled="!commentInput.trim() || isSubmitting"
        @click="handleSubmitComment"
      >
        发送
      </button>
    </div>
  </div>
</template>

<style scoped>
.post-detail-page {
  min-height: 100vh;
  background: var(--bg-color);
  padding-bottom: 80px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: white;
  border-bottom: 1px solid var(--border-color);
}

.back-btn {
  background: none;
  color: var(--text-color);
  font-size: 16px;
}

.header h1 {
  font-size: 18px;
  font-weight: 600;
}

.placeholder {
  width: 48px;
}

.loading,
.empty {
  text-align: center;
  padding: 40px 0;
  color: var(--text-light);
}

.content {
  padding: 16px;
}

.comments-section {
  margin-top: 16px;
  background: white;
  border-radius: 12px;
  padding: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.no-comments {
  text-align: center;
  color: var(--text-light);
  padding: 24px 0;
  font-size: 14px;
}

.comment-input-wrapper {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 12px 16px;
  display: flex;
  gap: 12px;
  border-top: 1px solid var(--border-color);
}

.comment-input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  font-size: 14px;
  outline: none;
}

.send-btn {
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  border-radius: 20px;
  font-size: 14px;
  transition: opacity 0.2s;
}

.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
