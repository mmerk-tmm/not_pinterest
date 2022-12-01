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
      path: '/new-art',
      name: 'Новый арт',
      component: () => import('../views/NewArtView.vue'),
    },
    {
      path: '/settings',
      name: 'Настройки',
      component: () => import('../views/SettingsView.vue'),
      children: [
        {
          path: 'edit-profile',
          name: 'Ректировать профиль',
          component: () => import('../components/Settings/EditProfile.vue'),
        },
        {
          path: 'personal-information',
          name: 'Персональные данные',
          component: () => import('../components/Settings/PersonalInformation.vue'),
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'Страница не найдена',
      alias: '/404',
      component: () => import('../views/404.vue')
    },
  ]
})
router.beforeEach((to, from, next) => {
  document.title = to.name;

  let flag = sessionStorage.getItem('logined');
  let role = sessionStorage.getItem('user-role');
  if (to.meta.requireAuth == true) {
    if (!flag || flag === 'false') {
      next({
        path: '/login'
      })
    } else {
      let roles = to.meta.roles;
      if (roles) {
        if (!role || roles.indexOf(role) < 0) {
          next({
            path: '/login'
          })
        } else {
          return next();
        }
      } else {
        return next();
      }
    }
  } else {
    return next();
  }
});

export default router
