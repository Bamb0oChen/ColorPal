<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import PostCard from '@/components/community/PostCard.vue'
import CommunityHeader from '@/components/community/CommunityHeader.vue'

const router = useRouter()
const communityStore = useCommunityStore()
const activeTab = ref('all')
const isInjecting = ref(false)

const handleInject = async () => {
  isInjecting.value = true
  try {
    await communityStore.injectPosts()
  } finally {
    isInjecting.value = false
  }
}

const tabs = [
  { id: 'all', label: '全部' },
  { id: 'hot', label: '热门' },
  { id: 'new', label: '最新' },
  { id: 'following', label: '关注' },
]

onMounted(() => {
  communityStore.fetchPosts()
})
</script>

<template>
  <div class="community-page">
    <CommunityHeader />

    <div class="tabs-wrapper">
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="tab-btn"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>
      <button class="inject-btn" :disabled="isInjecting" @click="handleInject">
        {{ isInjecting ? '注入中...' : '注入示例' }}
      </button>
    </div>

    <div class="post-list">
      <div v-if="communityStore.isLoading" class="loading-container">
        <div class="loading-spinner" />
        <span class="loading-text">正在加载色彩故事...</span>
      </div>
      <div v-else-if="communityStore.posts.length === 0" class="empty-container">
        <div class="empty-icon">
          <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="24" cy="24" r="20" />
            <path d="M16 24l4 4 8-8" />
          </svg>
        </div>
        <h3 class="empty-title">还没有色彩故事</h3>
        <p class="empty-desc">成为第一个分享色彩发现的人吧！</p>
        <button class="empty-btn" @click="router.push('/community/post')">
          立即分享
        </button>
      </div>
      <div v-else class="posts-container">
        <PostCard
          v-for="(post, index) in communityStore.posts"
          :key="post.id"
          :post="post"
          class="post-item"
          :style="{ animationDelay: `${index * 0.1}s` }"
          @like="communityStore.toggleLike"
          @click="router.push(`/community/post/${post.id}`)"
        />
      </div>
    </div>

    <button class="fab-btn" @click="router.push('/community/post')">
      <svg class="fab-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" />
        <path d="M8 12l2 2 4-4" />
      </svg>
      <span class="fab-text">发布</span>
    </button>
  </div>
</template>

<style scoped>
.community-page {
  min-height: 100vh;
  background: var(--color-bg);
  padding: 90px 0 100px;
}

@media (max-width: 760px) {
  .community-page {
    padding-top: 0;
  }
}

.tabs-wrapper {
  padding: 0 var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.inject-btn {
  flex-shrink: 0;
  height: 38px;
  padding: 0 14px;
  border: 1px solid rgba(20, 20, 20, 0.1);
  border-radius: var(--radius-sm);
  background: var(--color-white);
  color: var(--color-text-light);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.inject-btn:hover:not(:disabled) {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.inject-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.tabs {
  display: flex;
  gap: var(--spacing-sm);
  background: var(--color-white);
  padding: 4px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.tab-btn {
  flex: 1;
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--color-text-light);
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
}

.tab-btn.active {
  background: var(--color-primary);
  color: var(--color-white);
}

.post-list {
  padding: 0 var(--spacing-md);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 0;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: var(--color-text-light);
  font-size: 14px;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 0;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: var(--color-text-light);
  margin-bottom: var(--spacing-md);
}

.empty-title {
  margin: 0 0 4px;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text);
}

.empty-desc {
  margin: 0 0 var(--spacing-lg);
  font-size: 14px;
  color: var(--color-text-light);
}

.empty-btn {
  padding: var(--spacing-sm) var(--spacing-xl);
  background: var(--color-primary);
  color: var(--color-white);
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  box-shadow: var(--shadow-md);
}

.posts-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.post-item {
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
}

.fab-btn {
  position: fixed;
  right: var(--spacing-md);
  bottom: calc(var(--spacing-lg) + 60px);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-primary);
  color: var(--color-white);
  font-size: 15px;
  font-weight: 600;
  border: none;
  border-radius: 32px;
  cursor: pointer;
  box-shadow: var(--shadow-lg);
  transition: all 0.25s ease;
}

.fab-btn:hover {
  transform: translateY(-2px) scale(1.02);
}

.fab-icon {
  width: 20px;
  height: 20px;
}

.fab-text {
  letter-spacing: 0.5px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 760px) {
  .fab-btn {
    bottom: calc(var(--spacing-lg) + 80px);
  }
}
</style>
