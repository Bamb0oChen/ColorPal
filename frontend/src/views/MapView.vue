<script setup lang="ts">
import { ref, shallowRef, onMounted, watch } from 'vue'
import L from 'leaflet'
import gcoord from 'gcoord'
import RouteInputDialog from '@/components/RouteInputDialog.vue'
import { useLocation } from '@/composables/useLocation'
import { useRouteStore } from '@/stores/route'
import type { Location, Place } from '@/types/map'
import { parseRouteInput, type ColorRoutePoint, type ColorRouteSuggestion } from '@/types/route'

const { getCurrentLocation } = useLocation()
const routeStore = useRouteStore()
const AMAP_WEB_SERVICE_KEY = import.meta.env.VITE_AMAP_WEB_SERVICE_KEY?.trim() || ''
const FALLBACK_LOCATION = { lat: 30.310270426774228, lng: 120.08862685063117 }
let hasWarnedMissingAmapKey = false

type BrowserLocation = Location & { accuracy?: number }

const selectedPlace = ref<Place | null>(null)
const mapInstance = shallowRef<L.Map | null>(null)
const markers = shallowRef<L.Layer[]>([])
const routeMarkers = shallowRef<L.Layer[]>([])
const userLocationMarker = shallowRef<L.Marker | null>(null)
const currentLocation = ref<Location>({ ...FALLBACK_LOCATION })
const isLocating = ref(false)
const locationStatus = ref<'fallback' | 'requesting' | 'granted' | 'approximate' | 'failed'>('fallback')
const locationAccuracy = ref<number | null>(null)
const locationMessage = ref('')
const showLocationMessage = ref(false)
const showBottomSheet = ref(false)
const showRouteDialog = ref(false)
const searchQuery = ref('')
const searchInputRef = ref<HTMLInputElement | null>(null)
let locationMessageTimer: number | null = null

function showTemporaryLocationMessage(message: string, autoHide = true) {
  if (locationMessageTimer !== null) {
    window.clearTimeout(locationMessageTimer)
    locationMessageTimer = null
  }

  locationMessage.value = message
  showLocationMessage.value = true

  if (autoHide) {
    locationMessageTimer = window.setTimeout(() => {
      showLocationMessage.value = false
      locationMessage.value = ''
      locationMessageTimer = null
    }, 5000)
  }
}

async function handleSearch() {
  const q = searchQuery.value.trim()
  if (!q) return
  showBottomSheet.value = false
  selectedPlace.value = null
  await routeStore.suggestRoute(q, createRouteSuggestions)
  searchInputRef.value?.blur()
}

function clearSearch() {
  searchQuery.value = ''
  showBottomSheet.value = false
  selectedPlace.value = null
  routeStore.clearRoute()
}
const radiusOptions = [500, 1000, 3000, 5000, 10000]
const selectedRadius = ref(3000)
const radiusCircle = shallowRef<L.Circle | null>(null)

const wgs84ToGcj02 = (lat: number, lng: number): [number, number] => {
  const result = gcoord.transform([lng, lat], gcoord.WGS84, gcoord.GCJ02)
  return [result[1], result[0]]
}

const gcj02ToWgs84 = (lat: number, lng: number): [number, number] => {
  const result = gcoord.transform([lng, lat], gcoord.GCJ02, gcoord.WGS84)
  return [result[1], result[0]]
}

const EARTH_RADIUS_METERS = 6371000

const calculateDistance = (lat1: number, lng1: number, lat2: number, lng2: number): number => {
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLng = (lng2 - lng1) * Math.PI / 180
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return EARTH_RADIUS_METERS * c
}

function offsetLocation(origin: Location, distance: number, bearing: number): Location {
  const angularDistance = distance / EARTH_RADIUS_METERS
  const bearingRad = bearing * Math.PI / 180
  const latRad = origin.lat * Math.PI / 180
  const lngRad = origin.lng * Math.PI / 180
  const nextLat = Math.asin(
    Math.sin(latRad) * Math.cos(angularDistance) +
    Math.cos(latRad) * Math.sin(angularDistance) * Math.cos(bearingRad),
  )
  const nextLng = lngRad + Math.atan2(
    Math.sin(bearingRad) * Math.sin(angularDistance) * Math.cos(latRad),
    Math.cos(angularDistance) - Math.sin(latRad) * Math.sin(nextLat),
  )

  return {
    lat: nextLat * 180 / Math.PI,
    lng: nextLng * 180 / Math.PI,
  }
}

const updateRadiusCircle = () => {
  if (!mapInstance.value) return
  if (radiusCircle.value) mapInstance.value.removeLayer(radiusCircle.value)

  const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
  radiusCircle.value = L.circle([gcjLat, gcjLng], {
    radius: selectedRadius.value,
    color: '#64748b',
    fillColor: '#64748b',
    fillOpacity: 0.05,
    weight: 2,
    dashArray: '5,5',
  }).addTo(mapInstance.value)
  radiusCircle.value.bringToBack()
}

type PlaceColor = { hex: string; name: string }

const FALLBACK_PLACE_COLORS: PlaceColor[] = [
  { hex: '#50C878', name: '翠绿' },
  { hex: '#30D5C8', name: '湖蓝' },
  { hex: '#E1AD01', name: '芥末黄' },
  { hex: '#87CEEB', name: '天蓝' },
  { hex: '#FFBF00', name: '琥珀' },
  { hex: '#E34234', name: '朱红' },
  { hex: '#98FB98', name: '薄荷绿' },
  { hex: '#0047AB', name: '钴蓝' },
]

function getStableColor(text: string): PlaceColor {
  const sum = Array.from(text).reduce((total, char) => total + char.charCodeAt(0), 0)
  return FALLBACK_PLACE_COLORS[sum % FALLBACK_PLACE_COLORS.length]
}

function sanitizeColorKeywordText(text: string) {
  return text
    .replace(/紫金港|紫荆|紫金|紫云|紫竹/g, '')
    .toLowerCase()
}

/** 根据点位语义映射颜色，避免校区地名里的“紫”把所有点都染成紫色。 */
function mapColorByDescription(name: string, type: string): PlaceColor {
  const kw = sanitizeColorKeywordText(name + type)
  if (kw.includes('紫藤') || kw.includes('紫罗兰') || kw.includes('紫色') || kw.includes('purple') || kw.includes('violet')) {
    return { hex: '#8F00FF', name: '紫罗兰' }
  }
  if (kw.includes('餐饮') || kw.includes('咖啡') || kw.includes('饭') || kw.includes('面') || kw.includes('火锅') || kw.includes('烧烤') || kw.includes('小吃') || kw.includes('奶茶')) {
    return { hex: '#FFBF00', name: '琥珀' }
  }
  if (kw.includes('购物') || kw.includes('商场') || kw.includes('超市') || kw.includes('便利') || kw.includes('天街')) {
    return { hex: '#E34234', name: '朱红' }
  }
  if (kw.includes('学校') || kw.includes('学院') || kw.includes('大学') || kw.includes('教育') || kw.includes('图书')) {
    return { hex: '#0047AB', name: '钴蓝' }
  }
  if (kw.includes('酒店') || kw.includes('住宿') || kw.includes('公寓')) {
    return { hex: '#FFFDD0', name: '米黄' }
  }
  if (kw.includes('美容') || kw.includes('美甲') || kw.includes('spa') || kw.includes('生活服务')) {
    return { hex: '#98FB98', name: '薄荷绿' }
  }
  if (kw.includes('公司') || kw.includes('写字楼') || kw.includes('园区')) {
    return { hex: '#87CEEB', name: '天蓝' }
  }
  if (kw.includes('公园') || kw.includes('园林') || kw.includes('森林') || kw.includes('树林') || kw.includes('植') || kw.includes('绿') || kw.includes('湿地') || kw.includes('草')) {
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
  if (kw.includes('天空') || kw.includes('广场')) {
    return { hex: '#87CEEB', name: '天蓝' }
  }
  return getStableColor(name + type)
}

type NearbySearchOptions = {
  query?: string
  radius?: number
  pageLimit?: number
  center?: Location
  maxDistanceFromCurrent?: number
}

const COLOR_INTENTS = [
  { terms: ['红', 'red', '热烈'], hex: '#CC0000', name: '正红', label: '红色' },
  { terms: ['蓝', 'blue', '清新'], hex: '#0047AB', name: '钴蓝', label: '蓝色' },
  { terms: ['黄', '金', 'yellow', '温暖'], hex: '#FFD700', name: '金黄', label: '金色' },
  { terms: ['绿', 'green', '自然'], hex: '#50C878', name: '翠绿', label: '绿色' },
]

function getColorIntent(query: string): { hex: string; name: string; label: string } | null {
  const kw = query.toLowerCase()
  return COLOR_INTENTS.find((intent) => intent.terms.some((term) => kw.includes(term))) ?? null
}

function getAmapKeyword(query = '') {
  const trimmed = query.trim()
  return trimmed && !getColorIntent(trimmed) ? trimmed : ''
}

function getPageLimitForRadius(radius: number) {
  if (radius <= 1000) return 2
  if (radius <= 3000) return 4
  if (radius <= 5000) return 8
  return 12
}

function formatDistance(distance: number) {
  return distance >= 1000 ? `${(distance / 1000).toFixed(1)}km` : `${Math.round(distance)}m`
}

function formatRadius(radius: number) {
  return radius >= 1000 ? `${radius / 1000}km` : `${radius}m`
}

function isFarEnoughFromPicked(place: Place, picked: Place[], minDistance: number) {
  return picked.every((candidate) => (
    calculateDistance(
      place.location.lat,
      place.location.lng,
      candidate.location.lat,
      candidate.location.lng,
    ) >= minDistance
  ))
}

function selectDistributedPlaces(places: Place[], radius: number, limit: number) {
  const sorted = [...places].sort((a, b) => a.distance - b.distance)
  if (sorted.length <= limit) return sorted.slice(0, limit)

  const bands = [
    [radius * 0.68, radius + 1],
    [radius * 0.34, radius * 0.68],
    [0, radius * 0.34],
  ] as const
  const picked: Place[] = []
  const usedIds = new Set<string>()
  const perBand = Math.max(1, Math.ceil(limit / bands.length))
  const minDistance = Math.min(1400, Math.max(450, radius / 7))

  const tryPick = (candidates: Place[], quota: number, minSpacing: number) => {
    let pickedInBatch = 0
    candidates.some((place) => {
      if (picked.length >= limit || pickedInBatch >= quota) return true
      if (usedIds.has(place.id)) return false
      if (minSpacing > 0 && !isFarEnoughFromPicked(place, picked, minSpacing)) return false
      picked.push(place)
      usedIds.add(place.id)
      pickedInBatch += 1
      return false
    })
  }

  bands.forEach(([min, max]) => {
    const candidates = sorted.filter((place) => place.distance >= min && place.distance < max)
    tryPick(candidates, perBand, minDistance)
  })

  tryPick(sorted, limit - picked.length, minDistance)
  tryPick(sorted, limit - picked.length, Math.min(500, Math.max(180, radius / 30)))
  tryPick(sorted, limit - picked.length, 0)

  return picked
    .slice(0, limit)
    .sort((a, b) => a.distance - b.distance)
}

function calculateRouteDistance<T extends { location: Location }>(items: T[], origin: Location) {
  return items.reduce((total, item, index) => {
    const previous = index === 0 ? origin : items[index - 1].location
    return total + calculateDistance(
      previous.lat,
      previous.lng,
      item.location.lat,
      item.location.lng,
    )
  }, 0)
}

/** 点数很少时直接枚举，保证颜色路线的访问顺序尽量短。 */
function orderItemsByShortestPath<T extends { location: Location }>(items: T[], origin: Location) {
  if (items.length <= 2) return items

  let bestRoute = [...items]
  let bestDistance = calculateRouteDistance(bestRoute, origin)
  const used = new Set<number>()
  const currentRoute: T[] = []

  const search = () => {
    if (currentRoute.length === items.length) {
      const distance = calculateRouteDistance(currentRoute, origin)
      if (distance < bestDistance) {
        bestDistance = distance
        bestRoute = [...currentRoute]
      }
      return
    }

    items.forEach((item, index) => {
      if (used.has(index)) return
      used.add(index)
      currentRoute.push(item)
      search()
      currentRoute.pop()
      used.delete(index)
    })
  }

  search()
  return bestRoute
}

function createShortestFallbackSuggestions(input: string) {
  return parseRouteInput(input).map((suggestion) => {
    const points = orderItemsByShortestPath(suggestion.points, currentLocation.value)
      .map((point, index) => ({ ...point, order: index + 1 }))
    const distance = calculateRouteDistance(points, currentLocation.value)
    return {
      ...suggestion,
      description: `${suggestion.description} · 已按最短访问顺序排序，约 ${formatDistance(distance)}`,
      points,
    }
  })
}

const searchNearbyPlaces = async (options: NearbySearchOptions = {}): Promise<Place[]> => {
  const origin = currentLocation.value
  const searchCenter = options.center ?? origin
  const radius = options.radius ?? selectedRadius.value
  const maxDistanceFromCurrent = options.maxDistanceFromCurrent ?? radius
  const allSpots: Place[] = []
  const seenIds = new Set<string>()
  const maxPage = options.pageLimit ?? getPageLimitForRadius(radius)
  const offset = 25
  const keyword = getAmapKeyword(options.query)
  const [gcjLat, gcjLng] = wgs84ToGcj02(searchCenter.lat, searchCenter.lng)

  if (!AMAP_WEB_SERVICE_KEY) {
    if (!hasWarnedMissingAmapKey) {
      console.warn('[MapView] 未配置 VITE_AMAP_WEB_SERVICE_KEY，使用本地路线。')
      hasWarnedMissingAmapKey = true
    }
    return allSpots
  }

  try {
    for (let page = 1; page <= maxPage; page++) {
      const params = new URLSearchParams({
        key: AMAP_WEB_SERVICE_KEY,
        location: `${gcjLng},${gcjLat}`,
        radius: String(radius),
        offset: String(offset),
        page: String(page),
        extensions: 'all',
      })

      if (keyword) {
        params.set('keywords', keyword)
      } else {
        params.set('types', '050000|080000|110000|140000')
      }

      const url = `https://restapi.amap.com/v3/place/around?${params.toString()}`
      const response = await fetch(url)
      const data = await response.json()

      if (data.status !== '1' || !data.pois || data.pois.length === 0) break

      const spots = data.pois
        .filter((poi: any) => typeof poi.location === 'string' && poi.location.includes(','))
        .map((poi: any): Place => {
          const [poiLng, poiLat] = poi.location.split(',').map(Number)
          const [wgsLat, wgsLng] = gcj02ToWgs84(poiLat, poiLng)
          const rating = poi.biz_ext?.rating ? parseFloat(poi.biz_ext.rating) : 0
          const id = poi.id || `${poi.name}-${poi.location}`
          return {
            id,
            name: poi.name,
            address: poi.address || '',
            location: { lat: wgsLat, lng: wgsLng },
            category: 'scenic',
            rating,
            description: poi.type || '',
            image: '',
            distance: calculateDistance(origin.lat, origin.lng, wgsLat, wgsLng),
          }
        })
        .filter((place: Place) => (
          place.distance <= maxDistanceFromCurrent + 80 && !seenIds.has(place.id)
        ))

      spots.forEach((place: Place) => {
        allSpots.push(place)
        seenIds.add(place.id)
      })
      if (data.pois.length < offset) break
    }
    return allSpots.sort((a, b) => a.distance - b.distance)
  } catch {
    return allSpots
  }
}

function mergeUniquePlaces(groups: Place[][]) {
  const seenIds = new Set<string>()
  const merged: Place[] = []

  groups.flat().forEach((place) => {
    const key = place.id || `${place.name}-${place.location.lat.toFixed(5)}-${place.location.lng.toFixed(5)}`
    if (seenIds.has(key)) return
    const isSameSpot = merged.some((existing) => (
      calculateDistance(
        existing.location.lat,
        existing.location.lng,
        place.location.lat,
        place.location.lng,
      ) < 120
    ))
    if (isSameSpot) return
    seenIds.add(key)
    merged.push(place)
  })

  return merged.sort((a, b) => a.distance - b.distance)
}

async function searchPlacesAcrossRadius(options: NearbySearchOptions = {}): Promise<Place[]> {
  const radius = options.radius ?? selectedRadius.value
  if (options.center || radius <= 3000) {
    return searchNearbyPlaces(options)
  }

  const probeDistance = radius * 0.62
  const probeRadius = Math.min(2400, Math.max(900, radius * 0.3))
  const probePageLimit = radius >= 10000 ? 2 : 1
  const bearings = [0, 60, 120, 180, 240, 300]
  const probeSearches = bearings.map((bearing) => (
    searchNearbyPlaces({
      ...options,
      center: offsetLocation(currentLocation.value, probeDistance, bearing),
      radius: probeRadius,
      pageLimit: probePageLimit,
      maxDistanceFromCurrent: radius,
    })
  ))

  const groups = await Promise.all([
    searchNearbyPlaces({ ...options, maxDistanceFromCurrent: radius }),
    ...probeSearches,
  ])

  return mergeUniquePlaces(groups)
}

const searchNearbyScenicSpots = async (): Promise<Place[]> => {
  const spots = await searchPlacesAcrossRadius()
  return selectDistributedPlaces(spots, selectedRadius.value, 64)
}

async function createRouteSuggestions(input: string): Promise<ColorRouteSuggestion[]> {
  const radius = selectedRadius.value
  const places = await searchPlacesAcrossRadius({
    query: input,
    radius,
    pageLimit: getPageLimitForRadius(radius) + 2,
  })
  const routePlaces = orderItemsByShortestPath(
    selectDistributedPlaces(places, radius, 5),
    currentLocation.value,
  )
  if (routePlaces.length === 0) return createShortestFallbackSuggestions(input)

  const intent = getColorIntent(input)
  const firstColor = intent ?? mapColorByDescription(routePlaces[0].name, routePlaces[0].description)
  const routeDistance = calculateRouteDistance(routePlaces, currentLocation.value)
  const points = routePlaces.map((place, index): ColorRoutePoint => {
    const colorInfo = intent ?? mapColorByDescription(place.name, place.description)
    return {
      name: place.name,
      location: place.location,
      color: colorInfo.hex,
      colorName: colorInfo.name,
      description: `${place.address || place.description || '附近点位'} · ${formatDistance(place.distance)}`,
      order: index + 1,
    }
  })

  return [{
    title: `${intent?.label ?? input} · 附近色彩路线`,
    description: `基于当前位置 ${formatRadius(radius)} 内的真实点位生成，已按最短访问顺序排序，约 ${formatDistance(routeDistance)}`,
    themeColor: firstColor.hex,
    points,
  }]
}

function clearPlaceMarkers() {
  markers.value.forEach((m) => {
    mapInstance.value?.removeLayer(m)
  })
  markers.value = []
}

const refreshMarkers = async () => {
  if (!mapInstance.value) return
  clearPlaceMarkers()
  if (routeStore.hasActiveRoute) return

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
  if (userLocationMarker.value) {
    mapInstance.value.removeLayer(userLocationMarker.value)
  }
  const [gcjLat, gcjLng] = wgs84ToGcj02(currentLocation.value.lat, currentLocation.value.lng)
  const icon = L.divIcon({
    className: 'user-marker',
    html: `<div class="user-dot"></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10],
  })
  const popupText = locationStatus.value === 'granted' || locationStatus.value === 'approximate'
    ? '我的位置'
    : '推荐位置'
  userLocationMarker.value = L.marker([gcjLat, gcjLng], { icon })
    .addTo(mapInstance.value)
    .bindPopup(popupText)
}

function fitToRadius() {
  if (!mapInstance.value || !radiusCircle.value) return
  mapInstance.value.fitBounds(radiusCircle.value.getBounds(), { padding: [40, 40] })
}

async function applyLocation(loc: Location) {
  currentLocation.value = loc
  const [gcjLat, gcjLng] = wgs84ToGcj02(loc.lat, loc.lng)
  mapInstance.value?.setView([gcjLat, gcjLng], 15)
  addCurrentLocationMarker()
  updateRadiusCircle()
  if (routeStore.hasActiveRoute && searchQuery.value.trim()) {
    await handleSearch()
  } else {
    await refreshMarkers()
  }
}

const handleRadiusChange = async (radius: number) => {
  selectedRadius.value = radius
  updateRadiusCircle()
  fitToRadius()
  if (routeStore.hasActiveRoute && searchQuery.value.trim()) {
    await handleSearch()
  } else {
    await refreshMarkers()
  }
}

/** 在地图上渲染颜色路线点位 */
function renderRoutePoints(points: ColorRoutePoint[]) {
  routeMarkers.value.forEach((m) => {
    mapInstance.value?.removeLayer(m)
  })
  routeMarkers.value = []
  if (!mapInstance.value) return
  if (points.length === 0) {
    void refreshMarkers()
    return
  }
  clearPlaceMarkers()
  showBottomSheet.value = false
  selectedPlace.value = null

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
    const routeColor = points[0]?.color || '#ff6b6b'
    const halo = L.polyline(
      latlngs,
      { color: '#ffffff', weight: 8, opacity: 0.85 },
    ).addTo(mapInstance.value!)
    const line = L.polyline(
      latlngs,
      { color: routeColor, weight: 4, opacity: 0.95, dashArray: '10,8' },
    ).addTo(mapInstance.value!)
    halo.bringToFront()
    line.bringToFront()
    routeMarkers.value.push(halo)
    routeMarkers.value.push(line)
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
  if (isLocating.value) return
  isLocating.value = true
  locationStatus.value = 'requesting'
  showTemporaryLocationMessage('正在定位，请在浏览器弹窗中选择允许', false)
  try {
    const loc: BrowserLocation = await getCurrentLocation()
    locationAccuracy.value = loc.accuracy ?? null
    const isApproximate = loc.accuracy !== undefined && loc.accuracy > 1000
    locationStatus.value = isApproximate ? 'approximate' : 'granted'
    showTemporaryLocationMessage(isApproximate ? '定位成功' : '精确定位成功')
    await applyLocation(loc)
  } catch {
    locationStatus.value = 'failed'
    locationAccuracy.value = null
    showTemporaryLocationMessage('定位失败，请重试')
    await applyLocation(FALLBACK_LOCATION)
  } finally {
    isLocating.value = false
  }
}

onMounted(async () => {
  initMap()
  addCurrentLocationMarker()
  setTimeout(() => refreshMarkers(), 500)
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
        enterkeyhint="search"
        @keyup.enter="handleSearch"
      />
      <button
        type="button"
        class="search-submit"
        :disabled="!searchQuery.trim()"
        @click="handleSearch"
      >
        路线
      </button>
      <button
        v-if="searchQuery"
        type="button"
        class="search-clear"
        aria-label="清空路线"
        title="清空路线"
        @click="clearSearch"
      >
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

    <div class="location-control">
      <div v-if="showLocationMessage" :class="['location-toast', `status-${locationStatus}`]">
        <div class="location-copy">
          <span class="location-dot" />
          <span>{{ locationMessage }}</span>
        </div>
      </div>
      <button
        type="button"
        class="locate-btn"
        :disabled="isLocating"
        @click="handleLocate"
      >
        {{ isLocating ? '定位中...' : '点击定位' }}
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

.search-submit {
  flex-shrink: 0;
  padding: 6px 10px;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--color-primary);
  color: var(--color-white);
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
}

.search-submit:disabled {
  opacity: 0.45;
  cursor: not-allowed;
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

.location-control {
  position: absolute;
  top: 124px;
  left: 50%;
  transform: translateX(-50%);
  width: min(440px, calc(100% - 48px));
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 1000;
  pointer-events: none;
}

.location-toast {
  max-width: 100%;
  padding: 9px 12px;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid rgba(100, 116, 139, 0.18);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(10px);
  pointer-events: auto;
}

.location-copy {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.4;
  color: var(--color-text);
}

.location-dot {
  width: 9px;
  height: 9px;
  flex-shrink: 0;
  border-radius: 50%;
  background: #94a3b8;
  box-shadow: 0 0 0 4px rgba(148, 163, 184, 0.18);
}

.status-requesting .location-dot {
  background: #f59e0b;
  box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.18);
}

.status-granted .location-dot {
  background: #22c55e;
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.18);
}

.status-approximate .location-dot {
  background: #f97316;
  box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.18);
}

.status-failed .location-dot {
  background: #ef4444;
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.16);
}

.locate-btn {
  flex-shrink: 0;
  padding: 7px 10px;
  border: none;
  border-radius: var(--radius-sm);
  background: #1f2937;
  color: var(--color-white);
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: var(--shadow-md);
  pointer-events: auto;
}

.locate-btn:disabled {
  opacity: 0.6;
  cursor: wait;
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
