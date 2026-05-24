import { ref } from 'vue'

export const useLocation = () => {
  const currentLocation = ref<{ lat: number; lng: number } | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const getCurrentLocation = (): Promise<{ lat: number; lng: number }> => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('浏览器不支持定位'))
        return
      }

      isLoading.value = true
      error.value = null

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const loc = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy,
          }
          currentLocation.value = loc
          isLoading.value = false
          resolve(loc)
        },
        (err) => {
          error.value = err.message
          isLoading.value = false
          reject(err)
        },
        {
          enableHighAccuracy: true,
          timeout: 8000,
          maximumAge: 30000,
        },
      )
    })
  }

  return {
    currentLocation,
    isLoading,
    error,
    getCurrentLocation,
  }
}
