<script setup lang="ts">
import { computed } from 'vue'
import type { Post } from '@/types/community'

interface Props {
  post: Post
  showActions?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showActions: true,
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
      <div class="card-decoration" />
    </div>

    <div v-if="post.content" class="post-content">{{ post.content }}</div>

    <div v-if="post.images && post.images.length > 0" class="post-images" :class="{ single: post.images.length === 1 }">
      <div v-for="(img, index) in post.images" :key="index" class="image-wrapper">
        <img :src="img" class="post-image" alt="图片" />
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
        <svg class="action-icon" viewBox="0 0 24 24" :fill="post.liked ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
        <span>{{ post.likeCount }}</span>
      </button>
      <button class="action-btn">
        <svg class="action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
        <span>{{ post.commentCount }}</span>
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
  box-shadow: var(--shadow-sm);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
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
  pointer-events: none;
}

.post-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 107, 107, 0.12);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nickname {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
}

.time {
  font-size: 12px;
  color: var(--color-text-light);
}

.post-content {
  font-size: 15px;
  line-height: 1.7;
  color: var(--color-text);
  white-space: pre-wrap;
  margin-bottom: var(--spacing-sm);
}

.post-images {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: var(--spacing-sm);
}

.post-images.single {
  grid-template-columns: 1fr;
  max-width: 100%;
}

.image-wrapper {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.post-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.post-card:hover .post-image {
  transform: scale(1.05);
}

.color-info {
  background: var(--color-bg);
  border-radius: var(--radius-md);
  padding: var(--spacing-sm) var(--spacing-md);
  margin-bottom: var(--spacing-sm);
}

.color-info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.color-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-light);
  text-transform: uppercase;
}

.score-badge {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-primary);
}

.color-dots {
  display: flex;
  gap: 6px;
}

.color-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.06);
  position: relative;
}

.color-value {
  position: absolute;
  bottom: calc(100% + 4px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-text);
  color: white;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s ease;
}

.color-dot:hover .color-value {
  opacity: 1;
}

.post-actions {
  display: flex;
  gap: var(--spacing-lg);
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--color-border);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: var(--color-text-light);
  font-size: 13px;
  cursor: pointer;
  padding: 4px 0;
  transition: color 0.15s ease;
}

.action-btn:hover {
  color: var(--color-primary);
}

.action-btn.active {
  color: var(--color-primary);
}

.action-icon {
  width: 18px;
  height: 18px;
}
</style>
