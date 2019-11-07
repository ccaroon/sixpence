import Vue from 'vue'

import App from './App'
import router from './router'

import Vuetify from 'vuetify'
import('vuetify/dist/vuetify.min.css')
import('@mdi/font/css/materialdesignicons.min.css')
import('font-awesome/css/font-awesome.min.css')

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))

Vue.config.productionTip = false

Vue.use(Vuetify)

/* eslint-disable no-new */
new Vue({
  vuetify: new Vuetify({}),
  components: { App },
  router,
  // store,
  template: '<App/>'
}).$mount('#app')
