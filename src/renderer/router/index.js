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
      path: '/expenses/:month?',
      name: 'expenses-screen',
      component: require('@/components/Expenses').default
    },
    {
      path: '/reports',
      name: 'report-main',
      component: require('@/components/Report/Main').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
