<script setup lang="ts">
import { ref } from 'vue'
import { useSessionStore } from '@/stores/session'

const sessionStore = useSessionStore()
const displayName = ref('Color walker')

const handleLogin = async () => {
  await sessionStore.loginWithGithubDiscussion(displayName.value)
}
</script>

<template>
  <section class="login-panel" aria-labelledby="login-title">
    <p class="eyebrow">ColorPal</p>
    <h1 id="login-title">喂它颜色，陪它成长</h1>
    <p class="summary">使用 GitHub Discussions 进入色彩伙伴空间。</p>

    <label class="name-field">
      <span>昵称</span>
      <input v-model.trim="displayName" maxlength="40" placeholder="Color walker" />
    </label>

    <button class="login-button" type="button" :disabled="sessionStore.isLoading" @click="handleLogin">
      <span class="mark">GH</span>
      <span>{{ sessionStore.isLoading ? '正在连接 Discussion' : '通过 GitHub Discussion 登录' }}</span>
    </button>

    <p v-if="sessionStore.errorMessage" class="error">{{ sessionStore.errorMessage }}</p>
  </section>
</template>

<style scoped>
.login-panel {
  width: min(420px, calc(100vw - 40px));
  padding: 28px;
  border: 1px solid rgba(38, 38, 38, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.84);
  box-shadow: 0 24px 80px rgba(27, 27, 27, 0.08);
  backdrop-filter: blur(18px);
}

.eyebrow {
  margin: 0 0 16px;
  color: var(--accent-color);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0;
}

h1 {
  margin: 0;
  font-size: 34px;
  line-height: 1.08;
  letter-spacing: 0;
}

.summary {
  margin: 14px 0 24px;
  color: #686868;
  line-height: 1.7;
}

.name-field {
  display: grid;
  gap: 8px;
  margin-bottom: 16px;
  color: #555;
  font-size: 14px;
}

.name-field input {
  height: 44px;
  padding: 0 12px;
  border: 1px solid rgba(30, 30, 30, 0.14);
  border-radius: 6px;
  color: #202020;
  font: inherit;
  outline: none;
}

.name-field input:focus {
  border-color: var(--accent-color);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent-color), transparent 82%);
}

.login-button {
  width: 100%;
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border: 0;
  border-radius: 6px;
  background: #1f2328;
  color: #fff;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.login-button:disabled {
  cursor: progress;
  opacity: 0.74;
}

.mark {
  display: grid;
  width: 28px;
  height: 28px;
  place-items: center;
  border-radius: 50%;
  background: #fff;
  color: #1f2328;
  font-size: 11px;
}

.error {
  margin: 12px 0 0;
  color: #b3261e;
  font-size: 14px;
}
</style>
