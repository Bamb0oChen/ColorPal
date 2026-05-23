<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { checkHealth } from '@/api/health'

type Status = 'pending' | 'ok' | 'fail'

const status = ref<Status>('pending')
const serviceName = ref('')
const errorMessage = ref('')

const probe = async () => {
  status.value = 'pending'
  errorMessage.value = ''
  try {
    const result = await checkHealth()
    serviceName.value = result.service
    status.value = result.status === 'ok' ? 'ok' : 'fail'
  } catch (err) {
    status.value = 'fail'
    errorMessage.value = err instanceof Error ? err.message : String(err)
  }
}

onMounted(probe)
</script>

<template>
  <main class="hello">
    <h1>ColorPal</h1>
    <p class="tagline">喂它颜色，陪它成长，用新的方式看世界</p>

    <section class="health-card" :data-status="status">
      <h2>后端连通性</h2>
      <p v-if="status === 'pending'">检测中...</p>
      <p v-else-if="status === 'ok'">
        已连接 <code>{{ serviceName }}</code>
      </p>
      <p v-else>
        后端不可达
        <span v-if="errorMessage">：{{ errorMessage }}</span>
      </p>
      <button type="button" @click="probe">重新检测</button>
    </section>

    <p class="hint">这是脚手架页面，业务功能尚未实现。</p>
  </main>
</template>

<style scoped>
.hello {
  max-width: 480px;
  margin: 60px auto;
  padding: 24px;
  font-family: -apple-system, 'Helvetica Neue', sans-serif;
  text-align: center;
}

h1 {
  font-size: 48px;
  margin: 0 0 8px;
  color: #ff6b6b;
}

.tagline {
  color: #888;
  margin-bottom: 32px;
}

.health-card {
  padding: 24px;
  border-radius: 16px;
  background: #f8f9fa;
  text-align: left;
}

.health-card[data-status='ok'] {
  background: #e8f8f5;
}

.health-card[data-status='fail'] {
  background: #fdeaea;
}

.health-card h2 {
  margin-top: 0;
  font-size: 16px;
  color: #333;
}

code {
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SF Mono', Menlo, monospace;
}

button {
  margin-top: 12px;
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
}

.hint {
  margin-top: 32px;
  color: #bbb;
  font-size: 14px;
}
</style>
