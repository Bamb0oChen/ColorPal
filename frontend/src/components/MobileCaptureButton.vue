<script setup lang="ts">
const emit = defineEmits<{
  imageSelected: [file: File]
}>()

const handleFile = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) emit('imageSelected', file)
}
</script>

<template>
  <label class="capture-button">
    <input type="file" accept="image/*" capture="environment" @change="handleFile" />
    <span class="lens" />
  </label>
</template>

<style scoped>
.capture-button {
  width: 96px;
  height: 96px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background:
    radial-gradient(circle, #fff 0 42%, transparent 43%),
    conic-gradient(from 30deg, var(--accent-color), #ffd166, #4ecdc4, var(--accent-color));
  box-shadow: 0 18px 40px color-mix(in srgb, var(--accent-color), transparent 62%);
  cursor: pointer;
}

input {
  display: none;
}

.lens {
  width: 62px;
  height: 62px;
  border: 5px solid #fff;
  border-radius: 50%;
  background: color-mix(in srgb, var(--accent-color), white 62%);
}
</style>
