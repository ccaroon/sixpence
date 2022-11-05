import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../components/Main.vue'
import BlankSlate from '../components/BlankSlate.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'main',
    component: Main
  },
  {
    path: '/blank',
    name: 'blank-slate',
    component: BlankSlate
  }
]

const router = new VueRouter({
  routes
})

export default router
