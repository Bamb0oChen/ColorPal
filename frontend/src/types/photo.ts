export interface AnalysisResult {
  dominant_color: string
  palette: string[]
  score: number
  comment: string
  color_category: 'warm' | 'cool' | 'neutral'
  saturation_level: 'high' | 'medium' | 'low'
  brightness_level: 'high' | 'medium' | 'low'
}
