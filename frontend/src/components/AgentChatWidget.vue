<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { sendAgentMessage } from '@/api/agent'
import type { AgentChatHistoryItem, AgentMessage, AgentReplySource } from '@/types/agent'

const STORAGE_KEY = 'colorpal-agent-chat-v1'
const MAX_MESSAGES = 24
const HISTORY_LIMIT = 8

const router = useRouter()
const isOpen = ref(false)
const isSending = ref(false)
const draft = ref('')
const errorMessage = ref('')
const quickReplies = ref(['去拍照', '今日任务', '看看小彩状态'])
const messages = ref<AgentMessage[]>([])
const messageListRef = ref<HTMLElement | null>(null)

const hasFallbackReply = computed(() => {
  return messages.value.some((message) => message.source === 'fallback')
})

const visibleQuickReplies = computed(() => {
  const replies = ['去拍照', ...quickReplies.value.filter((reply) => reply !== '去拍照')]
  return [...new Set(replies)].slice(0, 4)
})

const createId = () => {
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

const createWelcomeMessage = (): AgentMessage => ({
  id: 'welcome',
  role: 'assistant',
  content:
    '嗨，我是小彩。你可以问我今天拍什么、我的能量状态，' +
    '或者让我们一起找一张高分颜色照片。',
})

const toHistory = (items: AgentMessage[]): AgentChatHistoryItem[] => {
  return items
    .filter((item) => item.role === 'user' || item.role === 'assistant')
    .slice(-HISTORY_LIMIT)
    .map(({ role, content }) => ({ role, content }))
}

const scrollToBottom = async () => {
  await nextTick()
  if (!messageListRef.value) return
  messageListRef.value.scrollTop = messageListRef.value.scrollHeight
}

const persistMessages = () => {
  const compactMessages = messages.value.slice(-MAX_MESSAGES)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(compactMessages))
}

const restoreMessages = () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (!saved) {
    messages.value = [createWelcomeMessage()]
    return
  }

  try {
    const parsed = JSON.parse(saved) as AgentMessage[]
    messages.value = parsed.length ? parsed.slice(-MAX_MESSAGES) : [createWelcomeMessage()]
  } catch {
    messages.value = [createWelcomeMessage()]
  }
}

const appendAssistantMessage = (content: string, source?: AgentReplySource) => {
  messages.value.push({
    id: createId(),
    role: 'assistant',
    content,
    source,
  })
}

const handleOpen = async () => {
  isOpen.value = true
  await scrollToBottom()
}

const handleMinimize = () => {
  isOpen.value = false
}

const handleClose = () => {
  isOpen.value = false
}

const handlePhotoEntry = async () => {
  isOpen.value = false
  await router.push('/')
  appendAssistantMessage(
    '我先把入口留在主页。等拍照页接好后，' +
    '那里会是进入色彩分析的主路径。',
  )
}

const sendMessage = async (content: string) => {
  const text = content.trim()
  if (!text || isSending.value) return

  const history = toHistory(messages.value)
  messages.value.push({
    id: createId(),
    role: 'user',
    content: text,
  })
  draft.value = ''
  errorMessage.value = ''
  isSending.value = true
  await scrollToBottom()

  try {
    const result = await sendAgentMessage({
      message: text,
      history,
      user_id: 'default',
    })
    appendAssistantMessage(result.reply, result.source)
    quickReplies.value = result.quick_replies.length ? result.quick_replies : quickReplies.value
  } catch (err) {
    console.error('[Agent Chat Error]', err)
    errorMessage.value = '小彩暂时连不上后端，稍后再试一次。'
    appendAssistantMessage(
      '我这边连线有点慢。你可以先去拍一张颜色明确的照片，' +
      '我恢复后再帮你看。',
      'fallback',
    )
  } finally {
    isSending.value = false
    await scrollToBottom()
  }
}

const handleSubmit = async () => {
  await sendMessage(draft.value)
}

const handleQuickReply = async (reply: string) => {
  if (reply === '去拍照') {
    await handlePhotoEntry()
    return
  }
  await sendMessage(reply)
}

onMounted(() => {
  restoreMessages()
})

watch(messages, persistMessages, { deep: true })
</script>

<template>
  <div class="agent-chat" :class="{ 'agent-chat--open': isOpen }">
    <button
      v-if="!isOpen"
      class="agent-chat__launcher"
      type="button"
      aria-label="打开小彩对话"
      @click="handleOpen"
    >
      <span class="agent-avatar" aria-hidden="true">
        <span class="agent-avatar__core"></span>
        <span class="agent-avatar__drop agent-avatar__drop--red"></span>
        <span class="agent-avatar__drop agent-avatar__drop--mint"></span>
        <span class="agent-avatar__drop agent-avatar__drop--yellow"></span>
      </span>
      <span class="agent-chat__launcher-text">
        <strong>小彩</strong>
        <span>问我今天拍什么</span>
      </span>
    </button>

    <section v-else class="agent-chat__panel" aria-label="小彩 Agent 对话框">
      <header class="agent-chat__header">
        <div class="agent-chat__identity">
          <span class="agent-avatar agent-avatar--small" aria-hidden="true">
            <span class="agent-avatar__core"></span>
            <span class="agent-avatar__drop agent-avatar__drop--red"></span>
            <span class="agent-avatar__drop agent-avatar__drop--mint"></span>
            <span class="agent-avatar__drop agent-avatar__drop--yellow"></span>
          </span>
          <div>
            <h2>小彩 Agent</h2>
            <p>
              <span class="agent-chat__status-dot"></span>
              在线陪你找颜色
              <span v-if="hasFallbackReply" class="agent-chat__source">本地兜底</span>
            </p>
          </div>
        </div>
        <div class="agent-chat__actions">
          <button type="button" aria-label="收起对话框" @click="handleMinimize">
            <svg viewBox="0 0 16 16" aria-hidden="true">
              <path d="M3 8h10" />
            </svg>
          </button>
          <button type="button" aria-label="关闭对话框" @click="handleClose">
            <svg viewBox="0 0 16 16" aria-hidden="true">
              <path d="M4 4l8 8M12 4l-8 8" />
            </svg>
          </button>
        </div>
      </header>

      <div ref="messageListRef" class="agent-chat__messages">
        <article
          v-for="message in messages"
          :key="message.id"
          class="agent-message"
          :class="`agent-message--${message.role}`"
        >
          <span v-if="message.role === 'assistant'" class="agent-message__mark" aria-hidden="true">
            <span></span>
          </span>
          <div class="agent-message__bubble">
            {{ message.content }}
            <em v-if="message.source === 'fallback'">本地回复</em>
          </div>
        </article>

        <article v-if="isSending" class="agent-message agent-message--assistant">
          <span class="agent-message__mark" aria-hidden="true">
            <span></span>
          </span>
          <div class="agent-message__bubble agent-message__bubble--typing">
            <i></i>
            <i></i>
            <i></i>
          </div>
        </article>
      </div>

      <div class="agent-chat__quick-replies" aria-label="快捷回复">
        <button
          v-for="reply in visibleQuickReplies"
          :key="reply"
          type="button"
          :disabled="isSending"
          @click="handleQuickReply(reply)"
        >
          {{ reply }}
        </button>
      </div>

      <p v-if="errorMessage" class="agent-chat__error">{{ errorMessage }}</p>

      <form class="agent-chat__composer" @submit.prevent="handleSubmit">
        <label class="agent-chat__input-wrap">
          <span class="sr-only">给小彩发送消息</span>
          <input
            v-model="draft"
            type="text"
            maxlength="500"
            placeholder="问小彩：今天拍什么颜色？"
            :disabled="isSending"
          />
        </label>
        <button class="agent-chat__send" type="submit" :disabled="isSending || !draft.trim()">
          <svg viewBox="0 0 20 20" aria-hidden="true">
            <path d="M3 10.5 16.5 3 12 17l-2.6-5.4L3 10.5Z" />
          </svg>
          <span class="sr-only">发送</span>
        </button>
      </form>
    </section>
  </div>
</template>

<style scoped>
.agent-chat {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 80;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
}

.agent-chat__launcher {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 220px;
  min-height: 64px;
  padding: 10px 14px 10px 10px;
  border: 1px solid rgba(80, 89, 122, 0.12);
  border-radius: 999px;
  color: #1d2433;
  background: #ffffff;
  box-shadow: 0 18px 48px rgba(33, 39, 67, 0.18);
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.agent-chat__launcher:hover {
  transform: translateY(-2px);
  box-shadow: 0 22px 56px rgba(33, 39, 67, 0.22);
}

.agent-chat__launcher-text {
  display: grid;
  gap: 2px;
  min-width: 0;
  text-align: left;
}

.agent-chat__launcher-text strong {
  font-size: 15px;
  line-height: 1.2;
}

.agent-chat__launcher-text span {
  overflow: hidden;
  color: #697084;
  font-size: 12px;
  line-height: 1.3;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.agent-avatar {
  position: relative;
  display: inline-grid;
  flex: 0 0 44px;
  width: 44px;
  height: 44px;
  place-items: center;
  border-radius: 16px;
  background:
    radial-gradient(circle at 32% 24%, rgba(255, 230, 109, 0.9), transparent 28px),
    linear-gradient(145deg, #5865f2, #2f80ed);
  box-shadow: inset 0 -8px 16px rgba(44, 65, 160, 0.18);
}

.agent-avatar--small {
  flex-basis: 40px;
  width: 40px;
  height: 40px;
  border-radius: 14px;
}

.agent-avatar__core {
  width: 21px;
  height: 21px;
  border-radius: 9px 12px 10px 14px;
  background: #ffffff;
  box-shadow: 0 5px 14px rgba(28, 35, 68, 0.2);
}

.agent-avatar__drop {
  position: absolute;
  width: 10px;
  height: 10px;
  border: 2px solid #ffffff;
  border-radius: 50%;
}

.agent-avatar__drop--red {
  right: 5px;
  top: 7px;
  background: #ff6b6b;
}

.agent-avatar__drop--mint {
  left: 6px;
  bottom: 7px;
  background: #4ecdc4;
}

.agent-avatar__drop--yellow {
  right: 9px;
  bottom: 4px;
  background: #ffe66d;
}

.agent-chat__panel {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto auto auto;
  width: min(388px, calc(100vw - 32px));
  height: min(640px, calc(100vh - 48px));
  overflow: hidden;
  border: 1px solid rgba(52, 63, 103, 0.12);
  border-radius: 22px;
  background: #ffffff;
  box-shadow: 0 28px 80px rgba(31, 37, 63, 0.24);
}

.agent-chat__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 76px;
  padding: 16px 16px 14px;
  border-bottom: 1px solid #edf0f6;
  background:
    linear-gradient(135deg, rgba(88, 101, 242, 0.08), transparent 45%),
    linear-gradient(90deg, rgba(78, 205, 196, 0.12), rgba(255, 230, 109, 0.1));
}

.agent-chat__identity {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 12px;
}

.agent-chat__identity h2 {
  margin: 0;
  color: #1d2433;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.2;
}

.agent-chat__identity p {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 4px 0 0;
  color: #697084;
  font-size: 12px;
  line-height: 1.3;
}

.agent-chat__status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #20c997;
  box-shadow: 0 0 0 3px rgba(32, 201, 151, 0.16);
}

.agent-chat__source {
  display: inline-flex;
  padding: 2px 6px;
  border-radius: 999px;
  color: #6d5600;
  background: rgba(255, 230, 109, 0.5);
  font-size: 11px;
}

.agent-chat__actions {
  display: flex;
  gap: 6px;
}

.agent-chat__actions button,
.agent-chat__send {
  display: inline-grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border: 0;
  border-radius: 11px;
  background: rgba(255, 255, 255, 0.74);
  color: #4d5874;
  cursor: pointer;
}

.agent-chat__actions button:hover,
.agent-chat__send:hover:not(:disabled) {
  background: #ffffff;
  color: #2f80ed;
}

.agent-chat__actions svg,
.agent-chat__send svg {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2;
}

.agent-chat__messages {
  min-height: 0;
  overflow-y: auto;
  padding: 18px 16px 16px;
  background:
    linear-gradient(180deg, rgba(247, 249, 252, 0.96), rgba(255, 255, 255, 0.94)),
    linear-gradient(90deg, rgba(255, 107, 107, 0.04), rgba(78, 205, 196, 0.04));
}

.agent-message {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  margin-bottom: 12px;
}

.agent-message--user {
  justify-content: flex-end;
}

.agent-message__mark {
  display: inline-grid;
  flex: 0 0 22px;
  width: 22px;
  height: 22px;
  place-items: center;
  border-radius: 8px;
  background: linear-gradient(145deg, #5865f2, #4ecdc4);
}

.agent-message__mark span {
  width: 10px;
  height: 10px;
  border-radius: 4px 6px 5px 7px;
  background: #ffffff;
}

.agent-message__bubble {
  max-width: min(282px, 78%);
  padding: 10px 12px;
  border: 1px solid #edf0f6;
  border-radius: 15px 15px 15px 5px;
  color: #283044;
  background: #ffffff;
  box-shadow: 0 8px 24px rgba(41, 48, 76, 0.08);
  font-size: 14px;
  line-height: 1.55;
  white-space: pre-wrap;
  word-break: break-word;
}

.agent-message--user .agent-message__bubble {
  border-color: transparent;
  border-radius: 15px 15px 5px;
  color: #ffffff;
  background: linear-gradient(135deg, #5865f2, #2f80ed);
  box-shadow: 0 10px 24px rgba(47, 128, 237, 0.22);
}

.agent-message__bubble em {
  display: block;
  width: fit-content;
  margin-top: 8px;
  padding: 2px 6px;
  border-radius: 999px;
  color: #796000;
  background: rgba(255, 230, 109, 0.45);
  font-size: 11px;
  font-style: normal;
}

.agent-message__bubble--typing {
  display: flex;
  gap: 4px;
  width: fit-content;
  min-width: 56px;
}

.agent-message__bubble--typing i {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #9aa4ba;
  animation: agentTyping 1.1s infinite ease-in-out;
}

.agent-message__bubble--typing i:nth-child(2) {
  animation-delay: 0.14s;
}

.agent-message__bubble--typing i:nth-child(3) {
  animation-delay: 0.28s;
}

.agent-chat__quick-replies {
  display: flex;
  gap: 8px;
  padding: 12px 14px 8px;
  overflow-x: auto;
  border-top: 1px solid #f2f4f8;
  background: #ffffff;
}

.agent-chat__quick-replies button {
  flex: 0 0 auto;
  max-width: 132px;
  overflow: hidden;
  padding: 8px 11px;
  border: 1px solid #dde4f0;
  border-radius: 999px;
  color: #435069;
  background: #ffffff;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}

.agent-chat__quick-replies button:hover:not(:disabled) {
  border-color: rgba(47, 128, 237, 0.42);
  color: #2f80ed;
  background: rgba(47, 128, 237, 0.06);
}

.agent-chat__quick-replies button:disabled,
.agent-chat__send:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.agent-chat__error {
  margin: 0;
  padding: 0 16px 8px;
  color: #c24150;
  background: #ffffff;
  font-size: 12px;
}

.agent-chat__composer {
  display: flex;
  gap: 10px;
  padding: 10px 14px 14px;
  background: #ffffff;
}

.agent-chat__input-wrap {
  flex: 1;
  min-width: 0;
}

.agent-chat__input-wrap input {
  width: 100%;
  height: 42px;
  padding: 0 14px;
  border: 1px solid #dde4f0;
  border-radius: 14px;
  outline: none;
  color: #1d2433;
  background: #f8faff;
  font: inherit;
  font-size: 14px;
}

.agent-chat__input-wrap input:focus {
  border-color: rgba(47, 128, 237, 0.54);
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.1);
}

.agent-chat__send {
  flex: 0 0 42px;
  width: 42px;
  height: 42px;
  border-radius: 14px;
  color: #ffffff;
  background: linear-gradient(135deg, #ff6b6b, #5865f2);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}

@keyframes agentTyping {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.45;
  }

  40% {
    transform: translateY(-3px);
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .agent-chat__launcher,
  .agent-message__bubble--typing i {
    animation: none;
    transition: none;
  }
}

@media (max-width: 640px) {
  .agent-chat {
    right: 12px;
    bottom: 12px;
    left: 12px;
  }

  .agent-chat__launcher {
    width: 100%;
    max-width: 260px;
    margin-left: auto;
  }

  .agent-chat__panel {
    width: 100%;
    height: min(620px, calc(100vh - 24px));
    border-radius: 20px;
  }

  .agent-message__bubble {
    max-width: 80%;
  }
}
</style>
