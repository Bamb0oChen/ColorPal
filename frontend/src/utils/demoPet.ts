import type { PetInfo } from '@/types/pet'

export function createDemoPet(color = '#ff6b6b'): PetInfo {
  return {
    name: '小彩',
    stage: 1,
    mood: 'happy',
    color,
    totalEnergy: 340,
    energy: {
      current: 58,
      max: 100,
      r: 34,
      g: 21,
      b: 18,
    },
  }
}
