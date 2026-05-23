<script setup lang="ts">
import { computed } from 'vue'
import type { Post } from '@/types/community'

interface Props {
  post: Post
  showActions?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showActions: true
})

const emit = defineEmits<{
  like: [postId: string]
  click: []
}>()

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

const handleLike = (e: Event) => {
  e.stopPropagation()
  emit('like', props.post.id)
}
</script>

<template>
  <article class="post-card" @click="emit('click')">
    <div class="post-header">
      <img :src="post.user.avatar" class="avatar" :alt="post.user.nickname" />
      <div class="user-info">
        <span class="nickname">{{ post.user.nickname }}</span>
        <span class="time">{{ formatTime(post.createdAt) }}</span>
      </div>
      <div class="card-decoration"></div>
    </div>

    <div v-if="post.content" class="post-content">{{ post.content }}</div>

    <div v-if="post.images && post.images.length > 0" class="post-images" :class="{ single: post.images.length === 1 }">
      <div
        v-for="(img, index) in post.images"
        :key="index"
        class="image-wrapper"
      >
        <img :src="img" class="post-image" alt="图片" />
        <div class="image-overlay"></div>
      </div>
    </div>

    <div v-if="post.photoRecord" class="color-info">
      <div class="color-info-header">
        <span class="color-label">色彩分析</span>
        <span class="score-badge">{{ post.photoRecord.score }}分</span>
      </div>
      <div class="color-dots">
        <div
          v-for="(color, index) in post.photoRecord.palette"
          :key="index"
          class="color-dot"
          :style="{ backgroundColor: color }"
          :title="color"
        >
          <span class="color-value">{{ color }}</span>
        </div>
      </div>
    </div>

    <div v-if="showActions" class="post-actions">
      <button class="action-btn" :class="{ active: post.liked }" @click="handleLike">
        <svg class="heart-icon" viewBox="0 0 24 24" :fill="post.liked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
        <span>{{ post.likeCount }}</span>
      </button>
      <button class="action-btn">
        <svg class="comment-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        <span>{{ post.commentCount }}</span>
      </button>
      <button class="action-btn share-btn">
        <svg class="share-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/>
          <polyline points="16 6 12 2 8 6"/>
          <line x1="12" y1="2" x2="12" y2="15"/>
        </svg>
      </button>
    </div>
  </article>
</template>

<style scoped>
.post-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  cursor: pointer;
  box-shadow: var(--shadow-card);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-decoration {
  position: absolute;
  top: -60px;
  right: -60px;
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.05) 0%, rgba(78, 205, 196, 0.05) 100%);
  border-radius: 50%;
}

.post-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  position: relative;
  z-index: 1;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 107, 107, 0.2);
  transition: transform var(--transition-fast);
}

.post-card:hover .avatar {
  transform: scale(1.05);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nickname {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-color);
}

.time {
  font-size: 12px;
  color: var(--text-light);
}

.post-content {
  font-size: 15px;
  line-height: 1.7;
  margin-bottom: var(--spacing-md);
  color: var(--text-color);
  position: relative;
  z-index: 1;
}

.post-images {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  position: relative;
  z-index: 1;
}

.post-images.single {
  grid-template-columns: 1fr;
}

.image-wrapper {
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.post-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.image-wrapper:hover .post-image {
  transform: scale(1.08);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 60%, rgba(0, 0, 0, 0.1) 100%);
  pointer-events: none;
}

.post-images.single .image-wrapper {
  aspect-ratio: 16 / 10;
}

.color-info {
  background: linear-gradient(135deg, #FFF9F9 0%, #F0F8F7 100%);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  border: 1px solid rgba(255, 107, 107, 0.1);
  position: relative;
  z-index: 1;
}

.color-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.color-label {
  font-size: 12px;
  color: var(--text-light);
  font-weight: 500;
}

.score-badge {
  font-size: 14px;
  font-weight: 700;
  color: var(--primary-color);
  background: rgba(255, 107, 107, 0.1);
  padding: 2px 10px;
  border-radius: 12px;
}

.color-dots {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.color-dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  position: relative;
  cursor: pointer;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.color-dot:hover {
  transform: scale(1.2);
  box-shadow: var(--shadow-md);
}

.color-dot:hover .color-value {
  opacity: 1;
  transform: translateY(0);
}

.color-value {
  position: absolute;
  bottom: -24px;
  left: 50%;
  transform: translateX(-50%) translateY(5px);
  font-size: 10px;
  color: var(--text-light);
  white-space: nowrap;
  opacity: 0;
  transition: all var(--transition-fast);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
}

.post-actions {
  display: flex;
  gap: var(--spacing-lg);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
  position: relative;
  z-index: 1;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  background: none;
  color: var(--text-light);
  font-size: 14px;
  padding: var(--spacing-sm) 0;
  transition: all var(--transition-fast);
  border-radius: var(--radius-sm);
}

.action-btn:hover {
  color: var(--primary-color);
  background: rgba(255, 107, 107, 0.05);
}

.action-btn.active {
  color: var(--primary-color);
}

.action-btn.active svg {
  animation: bounce 0.5s ease;
}

.share-btn:hover {
  color: var(--secondary-color);
  background: rgba(78, 205, 196, 0.05);
}

.heart-icon,
.comment-icon,
.share-icon {
  width: 20px;
  height: 20px;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}
</style>
