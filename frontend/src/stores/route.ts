/**
 * 颜色旅行路径状态管理
 *
 * 使用方式：
 *   const routeStore = useRouteStore()
 *   routeStore.suggestRoute(input)  // 输入链接或文字
 *   routeStore.activeRoute          // 当前选中的路线
 *   routeStore.selectRoute(index)   // 切换路线
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { parseRouteInput, type ColorRouteSuggestion } from '@/types/route'

export const useRouteStore = defineStore('route', () => {
  const suggestions = ref<ColorRouteSuggestion[]>([])
  const activeIndex = ref(0)
  const isProcessing = ref(false)

  const activeRoute = computed(() => suggestions.value[activeIndex.value] ?? null)

  const hasActiveRoute = computed(() => activeRoute.value !== null)

  /**
   * 输入链接/文字 → 解析 → 更新建议列表
   * 明日硬编码映射在 parseRouteInput 内部实现
   */
  async function suggestRoute(input: string) {
    isProcessing.value = true
    try {
      // 模拟异步（明日替换为真实逻辑）
      const result = await Promise.resolve(parseRouteInput(input))
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
