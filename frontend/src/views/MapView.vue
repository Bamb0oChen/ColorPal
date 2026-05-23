<script setup lang="ts">
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import gcoord from 'gcoord'
import { useLocation } from '@/composables/useLocation'
import type { Place } from '@/types/map'

const { getCurrentLocation } = useLocation()

const places = ref<Place[]>([])
const selectedPlace = ref<Place | null>(null)
const mapInstance = ref<L.Map | null>(null)
const markers = ref<L.Marker[]>([])
const currentLocation = ref<{ lat: number; lng: number }>({ lat: 0, lng: 0 })
const isLocating = ref(true)
const showBottomSheet = ref(false)
const radiusOptions = [500, 1000, 3000, 5000, 10000]
const selectedRadius = ref(3000)
const radiusCircle = ref<L.Circle | null>(null)

const wgs84ToGcj02 = (lat: number, lng: number): [number, number] => {
  const result = gcoord.transform([lng, lat], gcoord.WGS84, gcoord.GCJ02)
  return [result[1], result[0]]
}

const calculateDistance = (lat1: number, lng1: number, lat2: number, lng2: number): number => {
  const R = 6371000
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLng = (lng2 - lng1) * Math.PI / 180
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

const updateRadiusCircle = () => {
  if (!mapInstance.value) return
  
  if (radiusCircle.value) {
    mapInstance.value.removeLayer(radiusCircle.value)
  }
  
  const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
  radiusCircle.value = L.circle([gcjLat, gcjLng], {
    radius: selectedRadius.value,
    color: '#5B8FF9',
    fillColor: '#5B8FF9',
    fillOpacity: 0.1,
    weight: 2,
    dashArray: '5,5',
  }).addTo(mapInstance.value)
}

const searchNearbyScenicSpots = async (): Promise<Place[]> => {
  const { lat, lng } = currentLocation.value
  const radius = selectedRadius.value
  
  console.log(`搜索附近景点: 位置(${lat}, ${lng}), 半径: ${radius}m`)
  
  const allSpots: Place[] = []
  const maxPage = 2 // 最多请求2页
  const offset = 50 // 每页最多50条，总共100条
  
  try {
    for (let page = 1; page <= maxPage; page++) {
      const url = `https://restapi.amap.com/v3/place/around?key=ac61b3beda328566f7b6215a617629b6&location=${lng},${lat}&radius=${radius}&types=110000&offset=${offset}&page=${page}&extensions=all`
      console.log(`API请求URL(第${page}页):`, url)
      
      const response = await fetch(url)
      console.log('HTTP状态码:', response.status)
      
      const data = await response.json()
      console.log(`第${page}页 - API响应状态:`, data.status)
      
      if (data.status !== '1' || !data.pois || data.pois.length === 0) {
        console.log(`第${page}页 - 没有更多数据`)
        break
      }
      
      console.log(`第${page}页 - 景点数量:`, data.pois.length)
      
      const spots = data.pois.map((poi: any, index: number): Place => {
        const [poiLng, poiLat] = poi.location.split(',').map(Number)
        const rating = poi.biz_ext && poi.biz_ext.rating ? parseFloat(poi.biz_ext.rating) : (Math.random() * 1.5 + 3.5)
        return {
          id: poi.id || `spot-${page}-${index}`,
          name: poi.name,
          address: poi.address || '未知地址',
          location: { lat: poiLat, lng: poiLng },
          category: 'scenic',
          rating: rating,
          description: poi.type || '景点',
          image: `https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400`,
          distance: calculateDistance(lat, lng, poiLat, poiLng),
          duration: '计算中...',
        }
      }).filter(p => p.rating >= 4.2)
      
      allSpots.push(...spots)
      
      if (data.pois.length < offset) {
        console.log('已获取全部数据')
        break
      }
    }
    
    console.log(`总共找到 ${allSpots.length} 个符合条件的景点`)
    return allSpots
    
  } catch (error: any) {
    console.error('高德API调用失败:', error.message)
    console.error('错误详情:', error)
    return allSpots
  }
}

const getFilteredPlaces = (): Place[] => {
  console.log('当前位置:', currentLocation.value)
  console.log('搜索半径:', selectedRadius.value)
  console.log('景点总数:', places.value.length)
  
  const filtered = places.value
    .filter(place => {
      const distance = calculateDistance(
        currentLocation.value.lat,
        currentLocation.value.lng,
        place.location.lat,
        place.location.lng
      )
      const isScenic = place.category === 'scenic'
      const hasHighRating = place.rating >= 3.5
      const isWithinRadius = distance <= selectedRadius.value
      console.log(`景点: ${place.name}, 距离: ${(distance / 1000).toFixed(1)}km, 类别: ${place.category}, 评分: ${place.rating}, 符合条件: ${isScenic && hasHighRating && isWithinRadius}`)
      return isWithinRadius && isScenic && hasHighRating
    })
    .sort((a, b) => b.rating - a.rating)
  
  console.log('筛选结果:', filtered.map(p => p.name))
  return filtered
}

const refreshMarkers = async () => {
  console.log('refreshMarkers 被调用')
  console.log('地图实例:', mapInstance.value)
  
  if (!mapInstance.value) {
    console.error('地图实例不存在！')
    return
  }
  
  markers.value.forEach(marker => mapInstance.value?.removeLayer(marker))
  markers.value = []
  
  const nearbySpots = await searchNearbyScenicSpots()
  console.log('高德API搜索到的景点:', nearbySpots.length)
  
  nearbySpots.forEach((place, index) => {
    const [gcjLat, gcjLng] = wgs84ToGcj02(place.location.lat, place.location.lng)
    
    const marker = L.circleMarker([gcjLat, gcjLng], {
      radius: 16,
      fillColor: '#FF6B6B',
      color: '#FFFFFF',
      weight: 4,
      fillOpacity: 0.9,
    })
      .addTo(mapInstance.value!)
      .bindPopup(`<div style="padding: 8px;"><strong>${place.name}</strong><br>评分: ${place.rating.toFixed(1)}</div>`)
      .on('click', () => {
        selectPlace(place)
      })

    markers.value.push(marker)
    console.log(`标记已添加: ${place.name} at (${gcjLat}, ${gcjLng})`)
  })
}

const placeIcons: Record<string, string> = {
  scenic: '🌳',
  food: '🍽️',
  drink: '🥤',
  shopping: '🛍️',
  hotel: '🏨',
  default: '📍',
}

const initMap = () => {
  const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
  const map = L.map('map-container', {
    zoomControl: false,
    attributionControl: false,
  }).setView([gcjLat, gcjLng], 15)

  L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
    subdomains: ['1', '2', '3', '4'],
    maxZoom: 18,
    minZoom: 1,
    tileSize: 256,
    updateWhenIdle: true,
    updateWhenZooming: false,
    reuseTiles: true,
    zIndex: 0,
  }).addTo(map)

  mapInstance.value = map
  updateRadiusCircle()
}

const addCurrentLocationMarker = () => {
  if (!mapInstance.value) return

  const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
  const userIcon = L.divIcon({
    className: 'custom-user-marker',
    html: `<div style="width: 40px; height: 40px; background: var(--secondary); border: 4px solid white; border-radius: 50%; box-shadow: 0 4px 12px var(--shadow); display: flex; align-items: center; justify-content: center; font-size: 20px;">📍</div>`,
    iconSize: [40, 40],
    iconAnchor: [20, 20],
  })

  L.marker([gcjLat, gcjLng], { icon: userIcon })
    .addTo(mapInstance.value)
    .bindPopup('我的位置')
}

const addPlaceMarkers = () => {
  markers.value.forEach(marker => mapInstance.value?.removeLayer(marker))
  markers.value = []

  places.value.forEach((place, index) => {
    const [gcjLat, gcjLng] = wgs84ToGcj02(place.location.lat, place.location.lng)
    const color = index === 0 ? 'var(--primary)' : 'var(--secondary)'
    const icon = placeIcons[place.category] || placeIcons.default

    const placeIcon = L.divIcon({
      className: 'custom-place-marker',
      html: `
        <div style="
          background: ${color};
          border: 4px solid white;
          border-radius: 50%;
          width: 48px;
          height: 48px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;
          box-shadow: 0 4px 14px var(--shadow);
          position: relative;
        ">
          ${icon}
          ${index < 5 ? `<span style="position: absolute; top: -8px; right: -8px; background: white; color: var(--text-primary); width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; box-shadow: 0 2px 6px var(--shadow);">${index + 1}</span>` : ''}
        </div>
      `,
      iconSize: [48, 48],
      iconAnchor: [24, 24],
    })

    const marker = L.marker([gcjLat, gcjLng], { icon: placeIcon })
      .addTo(mapInstance.value!)
      .on('click', () => {
        selectPlace(place)
      })

    markers.value.push(marker)
  })
}

const selectPlace = (place: Place) => {
  selectedPlace.value = place
  showBottomSheet.value = true
  const [gcjLat, gcjLng] = wgs84ToGcj02(place.location.lat, place.location.lng)
  mapInstance.value?.setView([gcjLat, gcjLng], 15)
}

const handleRadiusChange = (radius: number) => {
  selectedRadius.value = radius
  updateRadiusCircle()
  refreshMarkers()
}

const handleLocate = async () => {
  try {
    const loc = await getCurrentLocation()
    currentLocation.value = loc
    const [gcjLat, gcjLng] = wgs84ToGcj02(loc.lat, loc.lng)
    mapInstance.value?.setView([gcjLat, gcjLng], 15)
    addCurrentLocationMarker()
    updateRadiusCircle()
    refreshMarkers()
  } catch (err) {
    console.error('定位失败:', err)
  }
}

onMounted(async () => {
  initMap()
  
  console.log('正在获取您的实时定位...')
  
  try {
    const loc = await getCurrentLocation()
    currentLocation.value = loc
    const [gcjLat, gcjLng] = wgs84ToGcj02(loc.lat, loc.lng)
    mapInstance.value?.setView([gcjLat, gcjLng], 15)
    updateRadiusCircle()
    addCurrentLocationMarker()
    console.log('✅ 实时定位成功:', loc)
    
    setTimeout(() => {
      refreshMarkers()
    }, 500)
  } catch (err) {
    console.error('❌ 定位失败:', err)
    alert('无法获取您的实时位置，请确保已授予定位权限。将使用默认位置。')
    // 如果定位失败，使用一个常见的默认位置（北京天安门附近）
    currentLocation.value = { lat: 39.9042, lng: 116.4074 }
    const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
    mapInstance.value?.setView([gcjLat, gcjLng], 15)
    updateRadiusCircle()
    addCurrentLocationMarker()
    
    setTimeout(() => {
      refreshMarkers()
    }, 500)
  } finally {
    isLocating.value = false
  }
})
</script>

<template>
  <div class="map-page">
    <div id="map-container" class="map-container"></div>

    <div class="radius-selector">
      <button
        v-for="radius in radiusOptions"
        :key="radius"
        @click="handleRadiusChange(radius)"
        :class="['radius-btn', { active: selectedRadius === radius }]"
      >
        {{ radius / 1000 }}km
      </button>
    </div>

    <div class="map-controls">
      <button @click="handleLocate" class="control-btn locate-btn">
        🎯
      </button>
      <button class="control-btn layers-btn">
        📊
      </button>
    </div>



    <div v-if="showBottomSheet && selectedPlace" class="bottom-sheet-overlay" @click="showBottomSheet = false">
      <div class="bottom-sheet" @click.stop>
        <div class="sheet-handle"></div>
        <img :src="selectedPlace.image" :alt="selectedPlace.name" class="sheet-image" />
        <div class="sheet-content">
          <h2 class="sheet-title">{{ selectedPlace.name }}</h2>
          <p class="sheet-address">{{ selectedPlace.address }}</p>
          <div class="sheet-rating">
            <span class="stars">⭐⭐⭐⭐⭐</span>
            <span class="rating-value">{{ selectedPlace.rating }}</span>
          </div>
          <p class="sheet-description">{{ selectedPlace.description }}</p>
          <div class="sheet-actions">
            <button class="action-btn primary">
              <span>📍</span>
              <span>导航</span>
            </button>
            <button class="action-btn secondary">
              <span>❤️</span>
              <span>收藏</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-page {
  width: 100%;
  height: 100vh;
  position: relative;
  background: var(--surface);
}

.map-container {
  width: 100%;
  height: 100%;
}

.radius-selector {
  position: absolute;
  top: 16px;
  left: 16px;
  display: flex;
  gap: 8px;
  background: white;
  padding: 8px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  z-index: 1000;
}

.radius-btn {
  padding: 8px 16px;
  border: 2px solid var(--border);
  border-radius: 12px;
  background: white;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.15s;
}

.radius-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.radius-btn:active {
  transform: scale(0.95);
}

.map-controls {
  position: absolute;
  right: 16px;
  bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 100;
}

.control-btn {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: white;
  border: 3px solid var(--border);
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 0 var(--border);
  transition: all 0.15s;
}

.control-btn:active {
  transform: translateY(4px);
  box-shadow: none;
}

.bottom-sheet-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 200;
  display: flex;
  align-items: flex-end;
  animation: fadeIn 0.2s;
}

.bottom-sheet {
  width: 100%;
  background: white;
  border-radius: 28px 28px 0 0;
  max-height: 75vh;
  overflow-y: auto;
  animation: slideUp 0.3s;
}

.sheet-handle {
  width: 48px;
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  margin: 14px auto;
}

.sheet-image {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

.sheet-content {
  padding: 20px;
}

.sheet-title {
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 8px;
}

.sheet-address {
  font-size: 15px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.sheet-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.stars {
  font-size: 18px;
}

.rating-value {
  font-size: 15px;
  font-weight: 700;
}

.sheet-description {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.sheet-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 700;
  border: none;
  transition: all 0.15s;
}

.action-btn.primary {
  background: var(--primary);
  color: white;
  box-shadow: 0 4px 0 var(--primary-dark);
}

.action-btn.primary:active {
  transform: translateY(4px);
  box-shadow: none;
}

.action-btn.secondary {
  background: white;
  color: var(--text-primary);
  border: 3px solid var(--border);
  box-shadow: 0 4px 0 var(--border);
}

.action-btn.secondary:active {
  transform: translateY(4px);
  box-shadow: none;
}

:deep(.custom-place-marker) {
  z-index: 100 !important;
  pointer-events: auto;
  width: 56px !important;
  height: 56px !important;
}

:deep(.custom-place-marker div) {
  z-index: 100 !important;
  width: 100% !important;
  height: 100% !important;
}

:deep(.custom-user-marker) {
  z-index: 99 !important;
  pointer-events: auto;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 10px 30px rgba(255, 107, 107, 0.7);
  }
}
</style>
