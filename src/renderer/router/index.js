import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../components/Main.vue'
import Placeholder from '../components/Placeholder.vue'
import Settings from '../components/Settings.vue'

Vue.use(VueRouter)

const routes = [
  {
    name: 'Main',
    path: '/',
    component: Main
  },
  {
    name: 'Budget',
    path: '/budget',
    component: Placeholder
  },
  {
    name: 'Expenses',
    path: '/expenses',
    component: Placeholder
  },
  {
    name: 'Reports',
    path: '/reports',
    component: Placeholder
  },
  {
    name: 'Settings',
    path: '/settings',
    component: Settings
  }
]

const router = new VueRouter({
  routes
})

export default router
