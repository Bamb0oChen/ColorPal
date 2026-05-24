<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import AgentChatWidget from '@/components/AgentChatWidget.vue'
import { usePaletteStore } from '@/stores/palette'
import { useSessionStore } from '@/stores/session'

const route = useRoute()
const router = useRouter()
const paletteStore = usePaletteStore()
const sessionStore = useSessionStore()

let touchStartX = 0
let touchStartY = 0

const navItems = [
  { label: '主页', name: 'home' },
  { label: '图鉴', name: 'collection' },
  { label: '地图', name: 'map' },
  { label: '社区', name: 'community' },
  { label: '我的', name: 'profile' },
]

const appStyle = computed(() => ({
  '--accent-color': paletteStore.accentColor,
}))

const handleTouchStart = (event: TouchEvent) => {
  if (!canSwipeNavigate() || event.touches.length !== 1) return
  touchStartX = event.touches[0].clientX
  touchStartY = event.touches[0].clientY
}

const handleTouchEnd = (event: TouchEvent) => {
  if (!canSwipeNavigate() || event.changedTouches.length !== 1) return

  const deltaX = event.changedTouches[0].clientX - touchStartX
  const deltaY = event.changedTouches[0].clientY - touchStartY

  if (Math.abs(deltaX) < 72 || Math.abs(deltaX) < Math.abs(deltaY) * 1.4) return

  const currentIndex = navItems.findIndex((item) => item.name === route.name)
  if (currentIndex < 0) return

  const nextIndex =
    deltaX < 0
      ? Math.min(navItems.length - 1, currentIndex + 1)
      : Math.max(0, currentIndex - 1)

  if (nextIndex !== currentIndex) {
    router.push({ name: navItems[nextIndex].name })
  }
}

const canSwipeNavigate = () =>
  sessionStore.isLoggedIn && window.matchMedia('(max-width: 760px)').matches
</script>

<template>
  <div class="app-shell" :style="appStyle">
    <header v-if="sessionStore.isLoggedIn" class="desktop-header">
      <RouterLink class="brand-link" :to="{ name: 'home' }">
        <span class="brand-mark" />
        <span>ColorPal</span>
      </RouterLink>

      <nav class="header-nav" aria-label="主导航">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          class="nav-link"
          :class="{ 'has-notice': item.name === 'collection' && paletteStore.hasCollectionNotice }"
          :to="{ name: item.name }"
        >
          {{ item.label }}
        </RouterLink>
      </nav>

      <button type="button" class="logout-button" @click="sessionStore.logout">退出</button>
    </header>

    <main class="route-stage" @touchstart.passive="handleTouchStart" @touchend.passive="handleTouchEnd">
      <RouterView />
    </main>

    <nav v-if="sessionStore.isLoggedIn" class="mobile-dots" aria-label="主导航">
      <RouterLink
        v-for="item in navItems"
        :key="item.name"
        class="dot-link"
        :class="{
          active: route.name === item.name,
          'has-notice': item.name === 'collection' && paletteStore.hasCollectionNotice,
        }"
        :to="{ name: item.name }"
        :aria-label="item.label"
      >
        <span class="dot" />
        <span class="dot-label">{{ item.label }}</span>
      </RouterLink>
    </nav>

    <AgentChatWidget />
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: color-mix(in srgb, var(--accent-color), #f8f9fa 94%);
}

.route-stage {
  min-height: 100vh;
}

.desktop-header {
  position: fixed;
  z-index: 20;
  top: 18px;
  left: 50%;
  width: min(1080px, calc(100vw - 48px));
  height: 58px;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 20px;
  padding: 0 16px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(18px);
  transform: translateX(-50%);
}

.brand-link,
.nav-link,
.dot-link {
  color: inherit;
  text-decoration: none;
}

.brand-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  font-weight: 850;
}

.brand-mark {
  width: 20px;
  height: 20px;
  border-radius: 5px;
  background:
    linear-gradient(135deg, var(--accent-color), transparent 72%),
    conic-gradient(from 90deg, #ff6b6b, #ffe66d, #4ecdc4, #74b9ff, #a29bfe, #ff6b6b);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.08);
}

.header-nav {
  display: inline-flex;
  gap: 6px;
  padding: 5px;
  border-radius: 7px;
  background: rgba(18, 18, 18, 0.04);
}

.nav-link {
  position: relative;
  min-width: 72px;
  padding: 9px 14px;
  border-radius: 6px;
  color: #555;
  font-size: 14px;
  font-weight: 700;
  text-align: center;
}

.nav-link.has-notice::after,
.dot-link.has-notice::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  border: 2px solid #fff;
  border-radius: 50%;
  background: #ff3b30;
  box-shadow: 0 4px 12px rgba(255, 59, 48, 0.36);
}

.nav-link.has-notice::after {
  top: 5px;
  right: 7px;
}

.nav-link.router-link-active {
  background: #fff;
  color: var(--accent-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.logout-button {
  justify-self: end;
  height: 36px;
  min-width: 64px;
  border: 1px solid rgba(30, 30, 30, 0.12);
  border-radius: 6px;
  background: #fff;
  color: #333;
  cursor: pointer;
}

.mobile-dots {
  position: fixed;
  z-index: 24;
  left: 50%;
  bottom: 14px;
  display: none;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.14);
  transform: translateX(-50%);
  backdrop-filter: blur(16px);
}

.dot-link {
  position: relative;
  display: grid;
  justify-items: center;
  gap: 4px;
  min-width: 40px;
  color: #777;
}

.dot-link.has-notice::after {
  top: -4px;
  right: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.dot-label {
  font-size: 11px;
  font-weight: 700;
}

.dot-link.active {
  color: var(--accent-color);
}

.dot-link.active .dot {
  width: 18px;
  border-radius: 999px;
}

@media (max-width: 760px) {
  .desktop-header {
    display: none;
  }

  .mobile-dots {
    display: inline-flex;
  }
}
</style>
