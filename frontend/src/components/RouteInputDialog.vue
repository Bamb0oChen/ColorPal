<script setup lang="ts">
import { ref } from 'vue'
import { useRouteStore } from '@/stores/route'

const emit = defineEmits<{
  close: []
  navigate: [index: number]
}>()

const routeStore = useRouteStore()
const inputText = ref('')
const inputMode = ref<'douyin' | 'text'>('douyin')

const handleSubmit = async () => {
  if (!inputText.value.trim()) return
  await routeStore.suggestRoute(inputText.value.trim())
  if (routeStore.hasActiveRoute) {
    emit('close')
  }
}
</script>

<template>
  <div class="route-overlay" @click.self="emit('close')">
    <div class="route-dialog">
      <div class="dialog-header">
        <h2>颜色旅行路线</h2>
        <button class="close-btn" @click="emit('close')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <p class="dialog-desc">
        粘贴抖音视频链接，或输入文字描述，自动生成基于颜色的旅行路线。
      </p>

      <div class="mode-tabs">
        <button
          :class="['mode-tab', { active: inputMode === 'douyin' }]"
          @click="inputMode = 'douyin'"
        >
          抖音链接
        </button>
        <button
          :class="['mode-tab', { active: inputMode === 'text' }]"
          @click="inputMode = 'text'"
        >
          文字输入
        </button>
      </div>

      <div class="input-area">
        <textarea
          v-model="inputText"
          :placeholder="inputMode === 'douyin'
            ? '粘贴抖音分享链接...'
            : '输入你想探索的颜色或主题...'"
          rows="3"
          class="text-input"
        />
      </div>

      <button
        class="submit-btn"
        :disabled="!inputText.trim() || routeStore.isProcessing"
        @click="handleSubmit"
      >
        {{ routeStore.isProcessing ? '分析中...' : '生成路线' }}
      </button>

      <!-- 路线结果列表 -->
      <div v-if="routeStore.suggestions.length > 0 && !routeStore.isProcessing" class="suggestions">
        <p class="suggestions-label">建议路线：</p>
        <button
          v-for="(route, index) in routeStore.suggestions"
          :key="index"
          :class="['route-card', { active: routeStore.activeIndex === index }]"
          @click="routeStore.selectRoute(index); emit('navigate', index)"
        >
          <span class="route-theme" :style="{ backgroundColor: route.themeColor }" />
          <div class="route-info">
            <strong>{{ route.title }}</strong>
            <span>{{ route.points.length }} 个站点 · {{ route.description }}</span>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.route-overlay {
  position: fixed;
  inset: 0;
  z-index: 300;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
}

.route-dialog {
  width: min(480px, 100%);
  max-height: 80vh;
  overflow-y: auto;
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-lg);
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
}

.dialog-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 750;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: var(--color-bg);
  color: var(--color-text);
  cursor: pointer;
  display: grid;
  place-items: center;
}

.dialog-desc {
  margin: 0 0 var(--spacing-md);
  font-size: 14px;
  color: var(--color-text-light);
  line-height: 1.6;
}

.mode-tabs {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.mode-tab {
  flex: 1;
  padding: 8px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-white);
  color: var(--color-text-light);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.mode-tab.active {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: color-mix(in srgb, var(--color-primary), transparent 92%);
}

.input-area {
  margin-bottom: var(--spacing-md);
}

.text-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: inherit;
  resize: none;
  outline: none;
  line-height: 1.6;
}

.text-input:focus {
  border-color: var(--color-primary);
}

.submit-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--color-primary);
  color: var(--color-white);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.15s ease;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.suggestions {
  margin-top: var(--spacing-md);
}

.suggestions-label {
  margin: 0 0 var(--spacing-sm);
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-light);
}

.route-card {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-white);
  cursor: pointer;
  margin-bottom: var(--spacing-sm);
  transition: all 0.15s ease;
}

.route-card.active {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--color-primary), transparent 70%);
}

.route-theme {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  flex-shrink: 0;
  border: 2px solid var(--color-white);
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.06);
}

.route-info {
  text-align: left;
  min-width: 0;
}

.route-info strong {
  display: block;
  font-size: 14px;
  margin-bottom: 2px;
}

.route-info span {
  display: block;
  font-size: 12px;
  color: var(--color-text-light);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 760px) {
  .route-dialog {
    max-height: 90vh;
    margin: auto 0 0;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  }
}
</style>
