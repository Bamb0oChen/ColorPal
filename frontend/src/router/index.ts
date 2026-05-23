import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/result',
      name: 'result',
      component: () => import('@/views/ResultView.vue'),
    },
    {
      path: '/map',
      name: 'map',
      component: () => import('@/views/MapView.vue'),
    },
    {
      path: '/collection',
      name: 'collection',
      component: () => import('@/views/CollectionView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('@/views/CommunityView.vue'),
    },
    {
      path: '/community/post',
      name: 'create-post',
      component: () => import('@/views/CreatePostView.vue'),
    },
    {
      path: '/community/post/:id',
      name: 'post-detail',
      component: () => import('@/views/PostDetailView.vue'),
    },
  ],
})

export default router
