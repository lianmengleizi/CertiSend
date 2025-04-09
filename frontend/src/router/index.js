import { createRouter, createWebHistory } from 'vue-router'
import MobileForm from '../pages/MobileForm.vue' // 根据真实路径调整
import AdminPage from '../pages/AdminTable.vue'

const routes = [
  {
    path: '/',
    name: 'MobileForm',
    component: MobileForm
  },
  {
    path: '/admin',
    name: 'AdminPage',
    component: AdminPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
