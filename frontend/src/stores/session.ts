import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { completeGithubDiscussionLogin, startGithubDiscussionLogin } from '@/api/auth'
import type { UserSession } from '@/types/auth'

const STORAGE_KEY = 'colorpal.session'

export const useSessionStore = defineStore('session', () => {
  const session = ref<UserSession | null>(loadSession())
  const isLoading = ref(false)
  const errorMessage = ref('')

  const isLoggedIn = computed(() => Boolean(session.value))

  const loginWithGithubDiscussion = async (displayName: string) => {
    isLoading.value = true
    errorMessage.value = ''
    const discussionTab = window.open('about:blank', '_blank')

    try {
      const start = await startGithubDiscussionLogin()
      if (discussionTab) {
        discussionTab.opener = null
        discussionTab.location.href = start.discussion_url
      } else {
        errorMessage.value = '浏览器阻止了 GitHub Discussion 窗口，请允许弹窗后重试'
        return
      }
      session.value = await completeGithubDiscussionLogin(displayName, start.discussion_url)
      localStorage.setItem(STORAGE_KEY, JSON.stringify(session.value))
    } catch (err) {
      errorMessage.value = err instanceof Error ? err.message : '登录失败，请重试'
      throw err
    } finally {
      isLoading.value = false
    }
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
