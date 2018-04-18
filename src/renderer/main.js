import Vue from 'vue'
// import axios from 'axios'

import App from './App'
import router from './router'
// import store from './store'

import Vuetify from 'vuetify'
import('vuetify/dist/vuetify.min.css')
import('mdi/css/materialdesignicons.min.css')
import('font-awesome/css/font-awesome.min.css')

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))

// Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false

Vue.use(Vuetify)

/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  // store,
  template: '<App/>'
}).$mount('#app')
