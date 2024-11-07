import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SettingsPage from '../views/SettingsPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    components: {
      default: Home
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    components: {
      default: SettingsPage
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 