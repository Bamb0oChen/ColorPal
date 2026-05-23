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

  for (const file of Array.from(files)) {
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
    return
  }

  isPublishing.value = true
  try {
    await communityStore.addPost({
      content: content.value,
      images: selectedImages.value,
    })
    router.back()
  } catch {
    // 发布失败提示
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
          <path d="M19 12H5m0 0l7-7m-7 7l7 7" />
        </svg>
      </button>
      <h1>分享色彩</h1>
      <button
        class="publish-btn"
        :disabled="isPublishing"
        @click="handlePublish"
      >
        <span v-if="isPublishing">发布中...</span>
        <span v-else>发布</span>
      </button>
    </header>

    <main class="content">
      <section class="editor-section">
        <div class="text-area-wrapper">
          <textarea
            v-model="content"
            class="text-area"
            placeholder="分享你发现的色彩故事..."
            rows="6"
            maxlength="500"
          />
          <div class="char-count">{{ content.length }}/500</div>
        </div>
      </section>

      <section class="image-upload-section">
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
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          </div>
          <label v-if="imagePreviews.length < 9" class="upload-btn">
            <input
              type="file"
              accept="image/*"
              multiple
              hidden
              @change="handleImageSelect"
            />
            <div class="upload-placeholder">
              <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
              <span>上传图片</span>
            </div>
          </label>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.create-post-page {
  min-height: 100vh;
  background: var(--color-bg);
  padding-bottom: 100px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-bg);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s ease;
}

.back-btn:hover {
  background: rgba(255, 107, 107, 0.1);
}

.back-icon {
  width: 20px;
  height: 20px;
  color: var(--color-text);
}

.header h1 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
}

.publish-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-primary);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  box-shadow: var(--shadow-md);
  transition: all 0.15s ease;
}

.publish-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.publish-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  border: none;
  border-radius: var(--radius-lg);
  background: transparent;
  font-size: 16px;
  line-height: 1.6;
  resize: none;
  outline: none;
  font-family: inherit;
  min-height: 120px;
}

.text-area::placeholder {
  color: var(--color-text-light);
}

.char-count {
  position: absolute;
  right: var(--spacing-md);
  bottom: var(--spacing-md);
  font-size: 12px;
  color: var(--color-text-light);
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
  color: var(--color-text);
}

.section-tip {
  font-size: 12px;
  color: var(--color-text-light);
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
  transition: transform 0.4s ease;
}

.image-preview:hover img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0);
  transition: background 0.15s ease;
}

.image-preview:hover .image-overlay {
  background: rgba(0, 0, 0, 0.5);
}

.remove-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.15s ease;
}

.image-preview:hover .remove-btn {
  opacity: 1;
  transform: scale(1);
}

.remove-btn:hover {
  background: var(--color-primary);
}

.remove-btn svg {
  width: 14px;
  height: 14px;
  color: white;
}

.upload-btn {
  display: block;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  border: 2px dashed var(--color-border);
  background: var(--color-bg);
  cursor: pointer;
  transition: all 0.15s ease;
}

.upload-btn:hover {
  border-color: var(--color-primary);
  background: rgba(255, 107, 107, 0.05);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: var(--spacing-xs);
  color: var(--color-text-light);
}

.upload-icon {
  width: 32px;
  height: 32px;
  color: var(--color-text-light);
}

.upload-placeholder span {
  font-size: 12px;
}
</style>
