<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community'
import PostCard from '@/components/community/PostCard.vue'
import CommunityHeader from '@/components/community/CommunityHeader.vue'

const router = useRouter()
const communityStore = useCommunityStore()
const activeTab = ref('all')

const tabs = [
  { id: 'all', label: '全部' },
  { id: 'hot', label: '热门' },
  { id: 'new', label: '最新' },
  { id: 'following', label: '关注' }
]

const stats = [
  { label: '今日活跃', value: '2.3k', icon: '🌍' },
  { label: '今日分享', value: '128', icon: '📸' },
  { label: '总用户', value: '15.6k', icon: '👥' }
]

onMounted(() => {
  communityStore.fetchPosts()
})
</script>

<template>
  <div class="community-page">
    <CommunityHeader />

    <div class="stats-bar">
      <div v-for="stat in stats" :key="stat.label" class="stat-item">
        <span class="stat-icon">{{ stat.icon }}</span>
        <div class="stat-info">
          <span class="stat-value">{{ stat.value }}</span>
          <span class="stat-label">{{ stat.label }}</span>
        </div>
      </div>
    </div>

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
    </div>

    <div class="post-list">
      <div v-if="communityStore.isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <span class="loading-text">正在加载色彩故事...</span>
      </div>
      <div v-else-if="communityStore.posts.length === 0" class="empty-container">
        <div class="empty-icon">🎨</div>
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
      <svg class="fab-icon" viewBox="0 0 24 24" fill="white" stroke="white" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <path d="M8 12l2 2 4-4"/>
      </svg>
      <span class="fab-text">发布</span>
    </button>
  </div>
</template>

<style scoped>
.community-page {
  min-height: 100vh;
  background: var(--gradient-bg);
  background-attachment: fixed;
  padding-bottom: 100px;
}

.stats-bar {
  display: flex;
  justify-content: space-around;
  padding: var(--spacing-md);
  background: white;
  margin: var(--spacing-md);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.stat-icon {
  font-size: 24px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-color);
}

.stat-label {
  font-size: 12px;
  color: var(--text-light);
}

.tabs-wrapper {
  padding: 0 var(--spacing-md);
  margin-bottom: var(--spacing-sm);
}

.tabs {
  display: flex;
  gap: var(--spacing-sm);
  background: white;
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
  color: var(--text-light);
  transition: all var(--transition-fast);
}

.tab-btn.active {
  background: var(--gradient-primary);
  color: white;
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
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  color: var(--text-light);
  font-size: 14px;
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 0;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
  animation: bounce 2s ease-in-out infinite;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-color);
  margin-bottom: var(--spacing-xs);
}

.empty-desc {
  font-size: 14px;
  color: var(--text-light);
  margin-bottom: var(--spacing-lg);
}

.empty-btn {
  padding: var(--spacing-sm) var(--spacing-xl);
  background: var(--gradient-primary);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border-radius: 24px;
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
  bottom: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--gradient-primary);
  color: white;
  font-size: 15px;
  font-weight: 600;
  border-radius: 32px;
  box-shadow: var(--shadow-lg);
  transition: all var(--transition-normal);
}

.fab-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: var(--shadow-lg);
}

.fab-icon {
  width: 20px;
  height: 20px;
}

.fab-text {
  letter-spacing: 0.5px;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
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
</style>
