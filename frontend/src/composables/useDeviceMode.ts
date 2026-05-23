import { onMounted, onUnmounted, ref } from 'vue'

export const useDeviceMode = () => {
  const isMobile = ref(false)

  const update = () => {
    isMobile.value = window.matchMedia('(max-width: 720px), (pointer: coarse)').matches
  }

  onMounted(() => {
    update()
    window.addEventListener('resize', update)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', update)
  })

  return { isMobile }
}
