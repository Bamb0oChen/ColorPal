import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'map',
    component: () => import('@/views/MapView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
