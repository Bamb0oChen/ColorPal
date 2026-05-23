import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { completeGithubDiscussionLogin, startGithubDiscussionLogin } from '@/api/auth'
import type { UserSession } from '@/types/auth'

const STORAGE_KEY = 'colorpal.session'
const DISCUSSION_URL = 'https://github.com/Bamb0oChen/ColorPal/discussions'

export const useSessionStore = defineStore('session', () => {
  const session = ref<UserSession | null>(loadSession())
  const isLoading = ref(false)
  const errorMessage = ref('')

  const isLoggedIn = computed(() => Boolean(session.value))

  const loginWithGithubDiscussion = async (displayName: string) => {
    isLoading.value = true
    errorMessage.value = ''

    try {
      const start = await startGithubDiscussionLogin()
      session.value = await completeGithubDiscussionLogin(displayName, start.discussion_url)
      persistSession(session.value)
      window.open(start.discussion_url, '_blank', 'noopener,noreferrer')
    } catch (err) {
      console.warn('[Auth] GitHub Discussion login failed, entering developer mode.', err)
      session.value = createLocalSession(displayName, 'developer_bypass')
      persistSession(session.value)
      errorMessage.value = 'GitHub 连接失败，已进入开发模式'
    } finally {
      isLoading.value = false
    }
  }

  const loginAsDeveloper = (displayName = 'Developer') => {
    errorMessage.value = ''
    session.value = createLocalSession(displayName, 'developer_bypass')
    persistSession(session.value)
  }

  const logout = () => {
    session.value = null
    localStorage.removeItem(STORAGE_KEY)
  }

  return {
    session,
    isLoading,
    errorMessage,
    isLoggedIn,
    loginWithGithubDiscussion,
    loginAsDeveloper,
    logout,
  }
})

function loadSession(): UserSession | null {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) return null

  try {
    return JSON.parse(raw) as UserSession
  } catch {
    localStorage.removeItem(STORAGE_KEY)
    return null
  }
}

function persistSession(session: UserSession) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(session))
}

function createLocalSession(displayName: string, provider: UserSession['provider']): UserSession {
  return {
    user_id: `dev-${createSessionId()}`,
    display_name: displayName.trim() || 'Developer',
    provider,
    discussion_url: DISCUSSION_URL,
    created_at: new Date().toISOString(),
  }
}

function createSessionId(): string {
  if ('crypto' in window && typeof window.crypto.randomUUID === 'function') {
    return window.crypto.randomUUID()
  }

  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`
}
