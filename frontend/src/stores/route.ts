/**
 * 颜色旅行路径状态管理
 *
 * 使用方式：
 *   const routeStore = useRouteStore()
 *   routeStore.suggestRoute(input, resolver)  // 输入链接或文字
 *   routeStore.activeRoute          // 当前选中的路线
 *   routeStore.selectRoute(index)   // 切换路线
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { parseRouteInput, type ColorRouteSuggestion } from '@/types/route'

type RouteSuggestionResolver = (
  input: string,
) => ColorRouteSuggestion[] | Promise<ColorRouteSuggestion[]>

export const useRouteStore = defineStore('route', () => {
  const suggestions = ref<ColorRouteSuggestion[]>([])
  const activeIndex = ref(0)
  const isProcessing = ref(false)

  const activeRoute = computed(() => suggestions.value[activeIndex.value] ?? null)

  const hasActiveRoute = computed(() => activeRoute.value !== null)

  async function suggestRoute(input: string, resolver?: RouteSuggestionResolver) {
    isProcessing.value = true
    try {
      const onlineResult = resolver ? await resolver(input) : []
      const result = onlineResult.length > 0 ? onlineResult : parseRouteInput(input)
      suggestions.value = result
      activeIndex.value = 0
    } finally {
      isProcessing.value = false
    }
  }

  function selectRoute(index: number) {
    if (index >= 0 && index < suggestions.value.length) {
      activeIndex.value = index
    }
  }

  function clearRoute() {
    suggestions.value = []
    activeIndex.value = 0
  }

  return {
    suggestions,
    activeRoute,
    activeIndex,
    isProcessing,
    hasActiveRoute,
    suggestRoute,
    selectRoute,
    clearRoute,
  }
})
