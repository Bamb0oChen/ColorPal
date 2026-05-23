<script setup lang="ts">
import type { Comment } from '@/types/community'

interface Props {
  comment: Comment
}

defineProps<Props>()

const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  return `${days}天前`
}
</script>

<template>
  <div class="comment-item">
    <img :src="comment.user.avatar" class="avatar" :alt="comment.user.nickname" />
    <div class="comment-content">
      <div class="comment-header">
        <span class="nickname">{{ comment.user.nickname }}</span>
        <span class="time">{{ formatTime(comment.createdAt) }}</span>
      </div>
      <div class="comment-bubble">
        <p class="text">{{ comment.content }}</p>
      </div>
      <div class="comment-actions">
        <button class="action-btn">
          <svg class="heart-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
          </svg>
        </button>
        <button class="action-btn reply-btn">回复</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comment-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-color);
}

.comment-item:last-child {
  border-bottom: none;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 107, 107, 0.15);
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.nickname {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-color);
}

.time {
  font-size: 12px;
  color: var(--text-light);
}

.comment-bubble {
  background: var(--bg-color);
  border-radius: 0 var(--radius-md) var(--radius-md) var(--radius-md);
  padding: var(--spacing-sm) var(--spacing-md);
  margin-bottom: var(--spacing-xs);
}

.text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-color);
  margin: 0;
}

.comment-actions {
  display: flex;
  gap: var(--spacing-lg);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  background: none;
  color: var(--text-light);
  font-size: 12px;
  padding: 4px 0;
  transition: color var(--transition-fast);
}

.action-btn:hover {
  color: var(--primary-color);
}

.heart-icon {
  width: 14px;
  height: 14px;
}

.reply-btn:hover {
  color: var(--secondary-color);
}
</style>
