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
      path: '/expenses/category/:category',
      name: 'expenses-screen-category',
      component: require('@/components/Expenses').default
    },
    {
      path: '/report/list',
      name: 'report-list',
      component: require('@/components/Report/Main').default
    },
    {
      path: '/report/yearly-budget/:year?',
      name: 'report-yearly-budget',
      component: require('@/components/Report/YearlyBudget').default
    },
    {
      path: '/report/multi-year-comparison',
      name: 'report-multi-year-comparison',
      component: require('@/components/Report/MultiYearComparison').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
