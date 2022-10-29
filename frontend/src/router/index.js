import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Главная',
      component: HomeView
    },
    {
      path: '/new-idea',
      name: 'Новый черновик',
      component: () => import('../views/NewIdeaView.vue'),
    },
    {
      path: '/settings',
      name: 'Настройки',
      component: () => import('../views/SettingsView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'Страница не найдена',
      alias: '/404',
      component: () => import('../views/404.vue')
    },
  ]
})

export default router
