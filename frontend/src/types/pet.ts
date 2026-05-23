export interface PetEnergy {
  current: number
  max: number
  r: number
  g: number
  b: number
}

export interface PetInfo {
  name: string
  stage: number
  mood: 'happy' | 'neutral' | 'sad'
  color: string
  energy: PetEnergy
}
