<script setup lang="ts">
</script>

<template>
  <header class="community-header">
    <div class="header-decoration"></div>
    <div class="header-content">
      <div class="title-section">
        <div class="logo-wrapper">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M8 12l2 2 4-4"/>
            </svg>
          </div>
          <h1>色彩社区</h1>
        </div>
        <button class="notification-btn">
          <svg class="bell-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <span class="badge">3</span>
        </button>
      </div>
      <div class="subtitle">发现身边的色彩，分享你的故事</div>
    </div>
  </header>
</template>

<style scoped>
.community-header {
  position: relative;
  background: var(--gradient-primary);
  padding: var(--spacing-lg) var(--spacing-md);
  overflow: hidden;
}

.header-decoration {
  position: absolute;
  top: -50%;
  right: -20%;
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  filter: blur(30px);
}

.header-content {
  position: relative;
  z-index: 1;
}

.title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}

.logo-wrapper {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.logo-icon svg {
  width: 24px;
  height: 24px;
}

.title-section h1 {
  font-size: 28px;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.notification-btn {
  position: relative;
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  transition: transform var(--transition-normal);
}

.notification-btn:hover {
  transform: scale(1.1);
}

.bell-icon {
  width: 20px;
  height: 20px;
  color: white;
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 18px;
  height: 18px;
  background: var(--accent-color);
  color: var(--text-color);
  font-size: 11px;
  font-weight: 600;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
}
</style>
