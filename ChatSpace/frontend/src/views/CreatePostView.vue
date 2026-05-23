<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCommunityStore } from '@/stores/community'

const router = useRouter()
const communityStore = useCommunityStore()

const content = ref('')
const selectedImages = ref<File[]>([])
const imagePreviews = ref<string[]>([])
const isPublishing = ref(false)

const handleImageSelect = (event: Event) => {
  const files = (event.target as HTMLInputElement).files
  if (!files) return

  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    if (selectedImages.value.length >= 9) break

    selectedImages.value.push(file)
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreviews.value.push(e.target?.result as string)
    }
    reader.readAsDataURL(file)
  }
}

const removeImage = (index: number) => {
  selectedImages.value.splice(index, 1)
  imagePreviews.value.splice(index, 1)
}

const handlePublish = async () => {
  if (!content.value.trim() && selectedImages.value.length === 0) {
    alert('请输入内容或上传图片')
    return
  }

  isPublishing.value = true
  try {
    await communityStore.addPost({
      content: content.value,
      images: selectedImages.value
    })
    router.back()
  } catch (err) {
    alert('发布失败，请重试')
  } finally {
    isPublishing.value = false
  }
}
</script>

<template>
  <div class="create-post-page">
    <header class="header">
      <button class="back-btn" @click="router.back()">
        <svg class="back-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5m0 0l7-7m-7 7l7 7"/>
        </svg>
      </button>
      <h1>分享色彩</h1>
      <button
        class="publish-btn"
        :disabled="isPublishing"
        @click="handlePublish"
      >
        <span v-if="isPublishing" class="loading-dots">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </span>
        <span v-else>发布</span>
      </button>
    </header>

    <main class="content">
      <div class="editor-section">
        <div class="text-area-wrapper">
          <textarea
            v-model="content"
            class="text-area"
            placeholder="分享你发现的色彩故事..."
            rows="6"
          />
          <div class="char-count">{{ content.length }}/500</div>
        </div>
      </div>

      <div class="image-upload-section">
        <div class="section-header">
          <span class="section-title">添加图片</span>
          <span class="section-tip">{{ imagePreviews.length }}/9</span>
        </div>
        <div class="image-grid">
          <div
            v-for="(preview, index) in imagePreviews"
            :key="index"
            class="image-preview"
          >
            <img :src="preview" alt="预览" />
            <div class="image-overlay">
              <button class="remove-btn" @click="removeImage(index)">
                <svg viewBox="0 0 24 24" fill="white" stroke="white" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
          </div>
          <label v-if="imagePreviews.length < 9" class="upload-btn">
            <input
              type="file"
              accept="image/*"
              multiple
              @change="handleImageSelect"
              hidden
            />
            <div class="upload-placeholder">
              <div class="upload-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
              </div>
              <span>上传图片</span>
            </div>
          </label>
        </div>
      </div>

      <div class="tips-section">
        <div class="tip-card">
          <span class="tip-icon">💡</span>
          <span class="tip-text">上传图片后，我们会自动分析图片的色彩搭配并给出评分哦~</span>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.create-post-page {
  min-height: 100vh;
  background: var(--gradient-bg);
  padding-bottom: 100px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-color);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.back-btn:hover {
  background: rgba(255, 107, 107, 0.1);
}

.back-icon {
  width: 20px;
  height: 20px;
  color: var(--text-color);
}

.header h1 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-color);
}

.publish-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--gradient-primary);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border-radius: 20px;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-fast);
}

.publish-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.publish-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-dots {
  display: flex;
  gap: 4px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: white;
  animation: loading 1s ease-in-out infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes loading {
  0%, 100% { opacity: 0.4; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1); }
}

.content {
  padding: var(--spacing-md);
}

.editor-section {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  margin-bottom: var(--spacing-md);
}

.text-area-wrapper {
  position: relative;
}

.text-area {
  width: 100%;
  padding: var(--spacing-md);
  padding-right: 80px;
  border: none;
  border-radius: var(--radius-lg);
  background: transparent;
  font-size: 16px;
  resize: none;
  outline: none;
  font-family: inherit;
  line-height: 1.6;
  min-height: 120px;
}

.text-area::placeholder {
  color: var(--text-light);
}

.char-count {
  position: absolute;
  right: var(--spacing-md);
  bottom: var(--spacing-md);
  font-size: 12px;
  color: var(--text-light);
}

.image-upload-section {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-color);
}

.section-tip {
  font-size: 12px;
  color: var(--text-light);
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-sm);
}

.image-preview {
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.image-preview:hover img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition-fast);
}

.image-preview:hover .image-overlay {
  background: rgba(0, 0, 0, 0.5);
}

.remove-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.8);
  transition: all var(--transition-fast);
}

.image-preview:hover .remove-btn {
  opacity: 1;
  transform: scale(1);
}

.remove-btn:hover {
  background: var(--primary-color);
}

.remove-btn svg {
  width: 14px;
  height: 14px;
}

.upload-btn {
  display: block;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  border: 2px dashed var(--border-color);
  background: var(--bg-color);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.upload-btn:hover {
  border-color: var(--primary-color);
  background: rgba(255, 107, 107, 0.05);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: var(--spacing-xs);
  color: var(--text-light);
}

.upload-icon {
  width: 32px;
  height: 32px;
  color: var(--text-light);
}

.upload-placeholder span {
  font-size: 12px;
}

.tips-section {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.05) 0%, rgba(78, 205, 196, 0.05) 100%);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  border: 1px solid rgba(255, 107, 107, 0.1);
}

.tip-card {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
}

.tip-icon {
  font-size: 18px;
}

.tip-text {
  font-size: 13px;
  color: var(--text-light);
  line-height: 1.5;
}
</style>
