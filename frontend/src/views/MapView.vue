<script setup lang="ts">
import { ref, shallowRef, onMounted, watch } from 'vue'
import L from 'leaflet'
import gcoord from 'gcoord'
import RouteInputDialog from '@/components/RouteInputDialog.vue'
import { useLocation } from '@/composables/useLocation'
import { useRouteStore } from '@/stores/route'
import type { Place } from '@/types/map'
import type { ColorRoutePoint } from '@/types/route'

const { getCurrentLocation } = useLocation()
const routeStore = useRouteStore()

const selectedPlace = ref<Place | null>(null)
const mapInstance = shallowRef<L.Map | null>(null)
const markers = shallowRef<L.Layer[]>([])
const routeMarkers = shallowRef<L.Layer[]>([])
const currentLocation = ref<{ lat: number; lng: number }>({ lat: 0, lng: 0 })
const isLocating = ref(true)
const showBottomSheet = ref(false)
const showRouteDialog = ref(false)
const searchQuery = ref('')
const searchInputRef = ref<HTMLInputElement | null>(null)

function handleSearch() {
  const q = searchQuery.value.trim()
  if (!q) return
  routeStore.suggestRoute(q)
  searchInputRef.value?.blur()
}
const radiusOptions = [500, 1000, 3000, 5000, 10000]
const selectedRadius = ref(3000)
const radiusCircle = shallowRef<L.Circle | null>(null)

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
  if (radiusCircle.value) mapInstance.value.removeLayer(radiusCircle.value)

  const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
  radiusCircle.value = L.circle([gcjLat, gcjLng], {
    radius: selectedRadius.value,
    color: '#ff6b6b',
    fillColor: '#ff6b6b',
    fillOpacity: 0.08,
    weight: 2,
    dashArray: '5,5',
  }).addTo(mapInstance.value)
}

/** 根据景点描述映射颜色 */
function mapColorByDescription(name: string, type: string): { hex: string; name: string } {
  const kw = (name + type).toLowerCase()
  if (kw.includes('公') || kw.includes('园') || kw.includes('林') || kw.includes('植') || kw.includes('绿')) {
    return { hex: '#7CFC00', name: '草绿' }
  }
  if (kw.includes('湖') || kw.includes('海') || kw.includes('水') || kw.includes('河') || kw.includes('江')) {
    return { hex: '#30D5C8', name: '湖蓝' }
  }
  if (kw.includes('宫') || kw.includes('殿') || kw.includes('城') || kw.includes('墙') || kw.includes('楼')) {
    return { hex: '#CC0000', name: '正红' }
  }
  if (kw.includes('桥') || kw.includes('塔') || kw.includes('台') || kw.includes('阁')) {
    return { hex: '#E1AD01', name: '芥末黄' }
  }
  if (kw.includes('寺') || kw.includes('庙') || kw.includes('庵') || kw.includes('观')) {
    return { hex: '#FFD700', name: '金黄' }
  }
  if (kw.includes('山') || kw.includes('峰') || kw.includes('岭') || kw.includes('石')) {
    return { hex: '#808000', name: '橄榄绿' }
  }
  if (kw.includes('天') || kw.includes('空') || kw.includes('广') || kw.includes('场')) {
    return { hex: '#87CEEB', name: '天蓝' }
  }
  return { hex: '#A29BFE', name: '淡紫' }
}

const searchNearbyScenicSpots = async (): Promise<Place[]> => {
  const { lat, lng } = currentLocation.value
  const radius = selectedRadius.value
  const allSpots: Place[] = []
  const maxPage = 2
  const offset = 50

  try {
    for (let page = 1; page <= maxPage; page++) {
      const url = `https://restapi.amap.com/v3/place/around?key=ac61b3beda328566f7b6215a617629b6&location=${lng},${lat}&radius=${radius}&types=110000&offset=${offset}&page=${page}&extensions=all`
      const response = await fetch(url)
      const data = await response.json()

      if (data.status !== '1' || !data.pois || data.pois.length === 0) break

      const spots = data.pois
        .map((poi: any): Place => {
          const [poiLng, poiLat] = poi.location.split(',').map(Number)
          const rating = poi.biz_ext?.rating ? parseFloat(poi.biz_ext.rating) : 0
          return {
            id: poi.id,
            name: poi.name,
            address: poi.address || '',
            location: { lat: poiLat, lng: poiLng },
            category: 'scenic',
            rating,
            description: poi.type || '',
            image: '',
            distance: calculateDistance(lat, lng, poiLat, poiLng),
          }
        })
        .filter((p: Place) => p.rating > 4.3)

      allSpots.push(...spots)
      if (data.pois.length < offset) break
    }
    return allSpots
  } catch {
    return allSpots
  }
}

const refreshMarkers = async () => {
  if (!mapInstance.value) return

  markers.value.forEach((m) => {
    mapInstance.value?.removeLayer(m)
  })
  markers.value = []

  const spots = await searchNearbyScenicSpots()
  spots.forEach((place) => {
    const [gcjLat, gcjLng] = wgs84ToGcj02(place.location.lat, place.location.lng)
    const colorInfo = mapColorByDescription(place.name, place.description)
    const marker = L.circleMarker([gcjLat, gcjLng], {
      radius: 14,
      fillColor: colorInfo.hex,
      color: '#fff',
      weight: 3,
      fillOpacity: 0.9,
    })
      .addTo(mapInstance.value!)
      .bindPopup(`<div style="padding:6px;font-size:13px"><strong>${place.name}</strong><br/>🎨 ${colorInfo.name}<br/>⭐ ${place.rating.toFixed(1)}</div>`)
      .on('click', () => { selectedPlace.value = place; showBottomSheet.value = true })

    markers.value.push(marker)
  })
}

const initMap = () => {
  const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
  const map = L.map('map-container', { zoomControl: false, attributionControl: false })
    .setView([gcjLat, gcjLng], 15)

  L.tileLayer('https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}', {
    subdomains: ['1', '2', '3', '4'],
    maxZoom: 18,
  }).addTo(map)

  mapInstance.value = map
  updateRadiusCircle()
}

const addCurrentLocationMarker = () => {
  if (!mapInstance.value) return
  const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
  const icon = L.divIcon({
    className: 'user-marker',
    html: `<div class="user-dot"></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  })
  L.marker([gcjLat, gcjLng], { icon }).addTo(mapInstance.value).bindPopup('我的位置')
}

const handleRadiusChange = (radius: number) => {
  selectedRadius.value = radius
  updateRadiusCircle()
  refreshMarkers()
}

/** 在地图上渲染颜色路线点位 */
function renderRoutePoints(points: ColorRoutePoint[]) {
  routeMarkers.value.forEach((m) => {
    mapInstance.value?.removeLayer(m)
  })
  routeMarkers.value = []
  if (!mapInstance.value || points.length === 0) return

  const latlngs: [number, number][] = []
  points.forEach((pt) => {
    const [gcjLat, gcjLng] = wgs84ToGcj02(pt.location.lat, pt.location.lng)
    latlngs.push([gcjLat, gcjLng])

    const icon = L.divIcon({
      className: 'route-marker',
      html: `<div class="route-dot" style="background:${pt.color}"><span class="route-label">${pt.order}</span></div>`,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
    })
    const marker = L.marker([gcjLat, gcjLng], { icon })
      .addTo(mapInstance.value!)
      .bindPopup(`<div style="font-size:13px"><strong>${pt.name}</strong><br/>${pt.colorName}<br/>${pt.description}</div>`)
    routeMarkers.value.push(marker)
  })

  // 画连线
  if (latlngs.length > 1) {
    L.polyline(latlngs, { color: '#ff6b6b', weight: 3, opacity: 0.6, dashArray: '8,8' }).addTo(mapInstance.value!)
  }

  // 缩放到路线范围
  mapInstance.value.fitBounds(latlngs, { padding: [50, 50] })
}

/** 监听路线变化自动更新地图 */
watch(() => routeStore.activeRoute, (route) => {
  if (route) renderRoutePoints(route.points)
  else renderRoutePoints([])
})

const handleLocate = async () => {
  try {
    const loc = await getCurrentLocation()
    currentLocation.value = loc
    const [gcjLat, gcjLng] = wgs84ToGcj02(loc.lat, loc.lng)
    mapInstance.value?.setView([gcjLat, gcjLng], 15)
    addCurrentLocationMarker()
    updateRadiusCircle()
    refreshMarkers()
  } catch { /* ignore */ }
}

onMounted(async () => {
  initMap()
  try {
    const loc = await getCurrentLocation()
    currentLocation.value = loc
    const [gcjLat, gcjLng] = wgs84ToGcj02(loc.lat, loc.lng)
    mapInstance.value?.setView([gcjLat, gcjLng], 15)
    updateRadiusCircle()
    addCurrentLocationMarker()
    setTimeout(() => refreshMarkers(), 500)
  } catch {
    currentLocation.value = { lat: 39.9042, lng: 116.4074 }
    const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
    mapInstance.value?.setView([gcjLat, gcjLng], 15)
    updateRadiusCircle()
    addCurrentLocationMarker()
    setTimeout(() => refreshMarkers(), 500)
  } finally {
    isLocating.value = false
  }
})
</script>

<template>
  <div class="map-page">
    <div id="map-container" class="map-container" />

    <!-- 搜索框 -->
    <div class="search-bar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" class="search-icon">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
      <input
        ref="searchInputRef"
        v-model="searchQuery"
        class="search-input"
        placeholder="输入颜色主题（红/蓝/金/绿）..."
        @keyup.enter="handleSearch"
      />
      <button v-if="searchQuery" class="search-clear" @click="searchQuery = ''; routeStore.clearRoute()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
          <line x1="18" y1="6" x2="6" y2="18" />
          <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      </button>
    </div>

    <RouteInputDialog
      v-if="showRouteDialog"
      @close="showRouteDialog = false"
      @navigate="showRouteDialog = false"
    />

    <div class="radius-selector">
      <button
        v-for="r in radiusOptions"
        :key="r"
        :class="['radius-btn', { active: selectedRadius === r }]"
        @click="handleRadiusChange(r)"
      >
        {{ r / 1000 }}km
      </button>
    </div>

    <div v-if="showBottomSheet && selectedPlace" class="sheet-overlay" @click="showBottomSheet = false">
      <div class="bottom-sheet" @click.stop>
        <div class="sheet-handle" />
        <div class="sheet-content">
          <h2 class="sheet-title">{{ selectedPlace.name }}</h2>
          <p class="sheet-addr">{{ selectedPlace.address }}</p>
          <div class="sheet-rating">
            <span>{{ selectedPlace.rating.toFixed(1) }} 分</span>
          </div>
          <p class="sheet-desc">{{ selectedPlace.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-page {
  width: 100%;
  height: calc(100vh - 76px);
  position: relative;
  margin-top: 76px;
  background: var(--color-bg);
}

.map-container {
  width: 100%;
  height: 100%;
}

.search-bar {
  position: absolute;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  width: min(420px, calc(100% - 48px));
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  background: var(--color-white);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  z-index: 1000;
  transition: box-shadow 0.15s ease;
}

.search-bar:focus-within {
  box-shadow: var(--shadow-lg);
}

.search-icon {
  flex-shrink: 0;
  color: var(--color-text-light);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  font-family: inherit;
  color: var(--color-text);
  background: transparent;
}

.search-input::placeholder {
  color: var(--color-text-light);
}

.search-clear {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 50%;
  background: var(--color-bg);
  color: var(--color-text-light);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radius-selector {
  position: absolute;
  top: 72px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
  background: var(--color-white);
  padding: 6px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  z-index: 1000;
}

.radius-btn {
  padding: 6px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-white);
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-light);
  cursor: pointer;
  transition: all 0.15s ease;
}

.radius-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-white);
}

.sheet-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 200;
  display: flex;
  align-items: flex-end;
}

.bottom-sheet {
  width: 100%;
  max-height: 50vh;
  overflow-y: auto;
  background: var(--color-white);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  animation: slideUp 0.25s ease;
}

.sheet-handle {
  width: 40px;
  height: 4px;
  border-radius: 2px;
  background: var(--color-border);
  margin: 12px auto;
}

.sheet-content {
  padding: 0 var(--spacing-lg) var(--spacing-lg);
}

.sheet-title {
  margin: 0 0 4px;
  font-size: 22px;
  font-weight: 750;
}

.sheet-addr {
  margin: 0 0 12px;
  font-size: 14px;
  color: var(--color-text-light);
}

.sheet-rating {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 12px;
}

.sheet-desc {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text-light);
}

:deep(.user-marker) {
  background: none !important;
  border: none !important;
}

:deep(.route-marker) {
  background: none !important;
  border: none !important;
}

:deep(.route-dot) {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.route-label) {
  color: #fff;
  font-size: 12px;
  font-weight: 800;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

:deep(.user-dot) {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--color-primary);
  border: 3px solid var(--color-white);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

:deep(.leaflet-popup-content-wrapper) {
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
}

:deep(.leaflet-popup-content) {
  margin: 8px 12px;
  font-size: 13px;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

@media (max-width: 760px) {
  .map-page {
    height: calc(100vh - 0px);
    margin-top: 0;
  }
}
</style>
