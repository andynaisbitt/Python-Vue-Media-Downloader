import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('../views/HomeView.vue')
        },
        {
          path: 'download',
          name: 'download',
          component: () => import('../views/DownloadView.vue'),
          meta: { 
            title: 'Download Center'
          }
        }
      ]
    },
    // Catch-all 404 route
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: { title: '404 Not Found' }
    }
  ]
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  // Update page title
  document.title = to.meta.title 
    ? `${to.meta.title} - YouTube Downloader`
    : 'YouTube Downloader'

  next()
})

// After navigation is confirmed
router.afterEach((to) => {
  // Scroll to top after navigation
  window.scrollTo(0, 0)
})

// Error handling
router.onError((error) => {
  console.error('Router error:', error)
  // You could redirect to an error page here
  router.push({ name: 'not-found' })
})

export default router