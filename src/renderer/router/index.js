import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main-screen',
      component: require('@/components/Main').default
    },
    {
      path: '/budget',
      name: 'budget-screen',
      component: require('@/components/Budget').default
    },
    {
      path: '/expenses',
      name: 'expenses-screen',
      component: require('@/components/Expenses').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
