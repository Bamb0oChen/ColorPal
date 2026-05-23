<template>
  <div class="profile-page">
    <!-- ====== 顶部：头像 + 个人信息 ====== -->
    <section class="profile-header">
      <div class="avatar-section">
        <div class="avatar">
          <img :src="user.avatar" alt="avatar" />
          <div class="avatar-badge" :style="{ background: levelColor }">
            Lv.{{ user.level }}
          </div>
        </div>
      </div>
      <div class="info-section">
        <h1 class="nickname">{{ user.nickname }}</h1>
        <p class="bio">{{ user.bio }}</p>
        <div class="stats-row">
          <div class="stat-item">
            <span class="stat-value">{{ user.stats.photos }}</span>
            <span class="stat-label">拍摄</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ user.stats.highestScore }}</span>
            <span class="stat-label">最高分</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ user.stats.colors }}</span>
            <span class="stat-label">已收集</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ user.stats.achievements }}</span>
            <span class="stat-label">成就</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ====== 收集总进度 ====== -->
    <section class="progress-bar-wrap">
      <div class="progress-header">
        <span>色彩收集进度</span>
        <span class="progress-text">{{ collectedCount }}/{{ totalCount }}</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
    </section>

    <!-- ====== 成就展示 ====== -->
    <section class="achievements-section">
      <div class="section-header">
        <h2>🏆 成就</h2>
        <span class="section-more">已完成 {{ doneCount }}/{{ achievements.length }}</span>
      </div>
      <div class="achievement-grid">
        <div
          v-for="a in achievements"
          :key="a.id"
          class="achievement-card"
          :class="{ unlocked: a.unlocked }"
        >
          <div class="achv-icon" :style="{ background: a.color + '22', color: a.color }">
            {{ a.icon }}
          </div>
          <div class="achv-info">
            <div class="achv-name">{{ a.name }}</div>
            <div class="achv-desc">{{ a.desc }}</div>
          </div>
          <div class="achv-status">
            <span v-if="a.unlocked" class="achv-done">✓</span>
            <span v-else class="achv-lock">{{ a.progress }}/{{ a.target }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ====== 设置 ====== -->
    <section class="settings-section">
      <h2>⚙️ 设置</h2>
      <div class="settings-list">
        <div v-for="s in settings" :key="s.key" class="setting-item" @click="handleSettingClick(s)">
          <span class="setting-icon">{{ s.icon }}</span>
          <span class="setting-label">{{ s.label }}</span>
          <span class="setting-arrow">›</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Stat {
  photos: number
  highestScore: number
  colors: number
  achievements: number
}

interface Achievement {
  id: string
  name: string
  desc: string
  icon: string
  color: string
  progress: number
  target: number
  unlocked: boolean
}

interface SettingItem {
  icon: string
  label: string
  key: string
  action?: () => void
}

const user = {
  nickname: '色彩猎人',
  avatar: 'data:image/svg+xml,' + encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="48" fill="#FF7E67"/>
      <circle cx="50" cy="38" r="18" fill="white"/>
      <ellipse cx="50" cy="72" rx="26" ry="22" fill="white"/>
      <circle cx="42" cy="35" r="3" fill="#2D3436"/>
      <circle cx="58" cy="35" r="3" fill="#2D3436"/>
      <path d="M 46 42 Q 50 46 54 42" stroke="#2D3436" stroke-width="2" fill="none" stroke-linecap="round"/>
    </svg>`
  ),
  bio: '用色彩记录世界',
  level: 5,
  stats: {
    photos: 128,
    highestScore: 95,
    colors: 18,
    achievements: 7,
  } as Stat,
}

const levelColor = '#A29BFE'

const totalCount = 36
const collectedCount = 18
const progressPercent = computed(() => (collectedCount / totalCount) * 100)

const achievements: Achievement[] = [
  // 收集类
  { id: 'red', name: '红色狂热', desc: '集齐全部6种红色系颜色', icon: '🔴', color: '#FF0000', progress: 3, target: 6, unlocked: false },
  { id: 'orange', name: '橙色收集家', desc: '集齐全部4种橙色系颜色', icon: '🟠', color: '#FFA500', progress: 4, target: 4, unlocked: true },
  { id: 'yellow', name: '黄色猎人', desc: '集齐全部5种黄色系颜色', icon: '🟡', color: '#FFD700', progress: 2, target: 5, unlocked: false },
  { id: 'green', name: '绿色守护者', desc: '集齐全部6种绿色系颜色', icon: '🟢', color: '#7CFC00', progress: 1, target: 6, unlocked: false },
  { id: 'blue', name: '蓝色梦想家', desc: '集齐全部6种蓝色系颜色', icon: '🔵', color: '#87CEEB', progress: 5, target: 6, unlocked: false },
  { id: 'purple', name: '紫色神秘', desc: '集齐全部5种紫色系颜色', icon: '🟣', color: '#8F00FF', progress: 0, target: 5, unlocked: false },
  { id: 'gray', name: '无彩大师', desc: '集齐全部4种无彩色/金属色', icon: '⚪', color: '#B2BEC3', progress: 1, target: 4, unlocked: false },
  { id: 'full', name: '全色谱大师', desc: '集齐全部36种颜色', icon: '🌈', color: '#FFD700', progress: 18, target: 36, unlocked: false },
  // 稀有度类
  { id: 'novice', name: '新手猎色', desc: '累计收集18种常见颜色', icon: '⭐', color: '#FFD700', progress: 12, target: 18, unlocked: false },
  { id: 'rare', name: '稀有发现者', desc: '累计收集11种稀有颜色', icon: '✨', color: '#74B9FF', progress: 4, target: 11, unlocked: false },
  { id: 'epic', name: '史诗猎手', desc: '累计收集5种史诗颜色', icon: '💎', color: '#A29BFE', progress: 2, target: 5, unlocked: false },
  { id: 'legend', name: '传说之眼', desc: '累计收集2种传说颜色', icon: '👑', color: '#FFD700', progress: 0, target: 2, unlocked: false },
  // 特殊组合
  { id: 'primary', name: '三原色', desc: '集齐正红+明黄+天蓝', icon: '🎨', color: '#00B894', progress: 2, target: 3, unlocked: false },
  { id: 'rainbow', name: '彩虹之路', desc: '集齐红橙黄绿蓝靛紫7色', icon: '🌈', color: '#00B894', progress: 4, target: 7, unlocked: false },
  { id: 'warmcool', name: '冷暖对决', desc: '同时拥有5种暖色+5种冷色', icon: '🔥', color: '#00B894', progress: 6, target: 10, unlocked: false },
  { id: 'bw', name: '黑白之间', desc: '集齐黑+白+银', icon: '⚫', color: '#00B894', progress: 1, target: 3, unlocked: false },
  { id: 'golden', name: '黄金时刻', desc: '日落时收集到金色或橙色', icon: '🌅', color: '#74B9FF', progress: 0, target: 1, unlocked: false },
]

const doneCount = computed(() => achievements.filter((a) => a.unlocked).length)

const settings: SettingItem[] = [
  { icon: '🎨', label: '我的精灵', key: 'pet' },
  { icon: '📷', label: '我的照片', key: 'photos' },
  { icon: '🗺️', label: '色彩足迹', key: 'map' },
  { icon: '🔔', label: '通知设置', key: 'notify' },
  { icon: '📖', label: '使用指南', key: 'guide' },
  { icon: 'ℹ️', label: '关于', key: 'about' },
]

function handleSettingClick(setting: SettingItem) {
  setting.action?.()
}
</script>

<style scoped>
.profile-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px 16px 48px;
  background: #FFFAF7;
  min-height: 100vh;
}

/* ====== 顶部 ====== */
.profile-header {
  display: flex;
  gap: 20px;
  align-items: center;
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  margin-bottom: 16px;
}

.avatar-section {
  flex-shrink: 0;
}

.avatar {
  position: relative;
  width: 80px;
  height: 80px;
}

.avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid #FF7E67;
  object-fit: cover;
  display: block;
}

.avatar-badge {
  position: absolute;
  bottom: -4px;
  right: -6px;
  color: white;
  font-size: 12px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 10px;
  white-space: nowrap;
}

.info-section {
  flex: 1;
  min-width: 0;
}

.nickname {
  font-size: 22px;
  font-weight: 700;
  color: #2D3436;
  margin: 0 0 2px;
}

.bio {
  font-size: 13px;
  color: #636E72;
  margin: 0 0 12px;
}

.stats-row {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #2D3436;
  line-height: 1.2;
}

.stat-label {
  font-size: 11px;
  color: #B2BEC3;
}

/* ====== 进度条 ====== */
.progress-bar-wrap {
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  margin-bottom: 16px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #636E72;
  margin-bottom: 8px;
}

.progress-text {
  font-weight: 600;
  color: #FF7E67;
}

.progress-track {
  height: 8px;
  background: #F0F0F0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #FF7E67, #FFD700);
  border-radius: 4px;
  transition: width 0.5s ease;
}

/* ====== 成就 ====== */
.achievements-section {
  margin-bottom: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-header h2 {
  font-size: 17px;
  font-weight: 600;
  color: #2D3436;
  margin: 0;
}

.section-more {
  font-size: 12px;
  color: #B2BEC3;
}

.achievement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 10px;
}

.achievement-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.2s;
  opacity: 0.7;
}

.achievement-card.unlocked {
  opacity: 1;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.achv-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.achv-info {
  flex: 1;
  min-width: 0;
}

.achv-name {
  font-size: 14px;
  font-weight: 600;
  color: #2D3436;
}

.achv-desc {
  font-size: 11px;
  color: #B2BEC3;
  margin-top: 1px;
}

.achv-status {
  flex-shrink: 0;
  font-size: 12px;
}

.achv-done {
  color: #00B894;
  font-weight: 700;
  font-size: 18px;
}

.achv-lock {
  color: #B2BEC3;
}

/* ====== 设置 ====== */
.settings-section h2 {
  font-size: 17px;
  font-weight: 600;
  color: #2D3436;
  margin: 0 0 12px;
}

.settings-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  cursor: pointer;
  transition: background 0.15s;
  border-bottom: 1px solid #F0F0F0;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-item:hover {
  background: #FFF5F0;
}

.setting-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.setting-label {
  flex: 1;
  font-size: 14px;
  color: #2D3436;
}

.setting-arrow {
  color: #B2BEC3;
  font-size: 20px;
}

/* ====== 响应式 ====== */
@media (max-width: 600px) {
  .profile-page {
    padding: 16px 12px 32px;
  }
  .profile-header {
    flex-direction: column;
    text-align: center;
    padding: 20px 16px;
  }
  .stats-row {
    justify-content: center;
  }
  .achievement-grid {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 900px) {
  .achievement-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
