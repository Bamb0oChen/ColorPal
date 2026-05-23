<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  imageSelected: [file: File]
}>()

const isDragging = ref(false)

const pickFile = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) emit('imageSelected', file)
}

const handleDrop = (event: DragEvent) => {
  isDragging.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file?.type.startsWith('image/')) emit('imageSelected', file)
}
</script>

<template>
  <label
    class="drop-zone"
    :class="{ 'is-dragging': isDragging }"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <input type="file" accept="image/*" @change="pickFile" />
    <span class="drop-icon">+</span>
    <span class="drop-title">把图片拖到这里</span>
    <span class="drop-caption">或点击选择一张照片</span>
  </label>
</template>

<style scoped>
.drop-zone {
  width: min(460px, calc(100vw - 48px));
  min-height: 170px;
  display: grid;
  place-items: center;
  align-content: center;
  gap: 10px;
  border: 1.5px dashed color-mix(in srgb, var(--accent-color), #d5d5d5 52%);
  border-radius: 8px;
  background: color-mix(in srgb, var(--accent-color), white 92%);
  color: #282828;
  cursor: pointer;
  transition:
    border-color 180ms ease,
    background 180ms ease,
    transform 180ms ease;
}

.drop-zone.is-dragging {
  border-color: var(--accent-color);
  background: color-mix(in srgb, var(--accent-color), white 84%);
  transform: translateY(-2px);
}

input {
  display: none;
}

.drop-icon {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: #fff;
  color: var(--accent-color);
  font-size: 30px;
  line-height: 1;
}

.drop-title {
  font-weight: 800;
}

.drop-caption {
  color: #777;
  font-size: 14px;
}
</style>
