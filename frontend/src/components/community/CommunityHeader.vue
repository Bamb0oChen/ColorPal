<script setup lang="ts">
</script>

<template>
  <header class="community-header">
    <div class="header-decoration" />
    <div class="header-content">
      <p class="eyebrow">Community</p>
      <h1>色彩社区</h1>
      <p class="subtitle">发现身边的色彩，分享你的故事</p>
    </div>
  </header>
</template>

<style scoped>
.community-header {
  position: relative;
  padding: 24px 20px;
  overflow: hidden;
}

.header-decoration {
  position: absolute;
  top: -50%;
  right: -20%;
  width: 200px;
  height: 200px;
  background: color-mix(in srgb, var(--color-primary), transparent 72%);
  border-radius: 50%;
  filter: blur(30px);
}

.header-content {
  position: relative;
  z-index: 1;
}

.eyebrow {
  margin: 0;
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 850;
  text-transform: uppercase;
}

h1 {
  margin: 8px 0 0;
  font-size: 28px;
  font-weight: 750;
  letter-spacing: -0.5px;
}

.subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: var(--color-text-light);
}
</style>
