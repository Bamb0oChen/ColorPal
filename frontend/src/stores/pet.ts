import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getProfile } from '@/api/user'
import { getStageFromXP, getStageXPProgress } from '@/utils/constants'
import type { PetInfo } from '@/types/pet'

export const usePetStore = defineStore('pet', () => {
  const petInfo = ref<PetInfo | null>(null)
  const isLoading = ref(false)

  const energyPercent = computed(() => {
    if (!petInfo.value) return 0
    return Math.round((petInfo.value.energy.current / petInfo.value.energy.max) * 100)
  })

  /** 由累计经验值 computed 出的阶段 */
  const stageInfo = computed(() => {
    const total = petInfo.value?.totalEnergy ?? 0
    return getStageXPProgress(total)
  })

  const fetchProfile = async () => {
    isLoading.value = true
    try {
      const profile = await getProfile()
      petInfo.value = profile.pet
    } finally {
      isLoading.value = false
    }
  }

  const updateEnergy = (change: { r: number; g: number; b: number; total: number }) => {
    if (!petInfo.value) return
    petInfo.value.energy.r += change.r
    petInfo.value.energy.g += change.g
    petInfo.value.energy.b += change.b
    petInfo.value.energy.current += change.total
    petInfo.value.totalEnergy += change.total
  }

  return { petInfo, isLoading, energyPercent, stageInfo, fetchProfile, updateEnergy }
})
