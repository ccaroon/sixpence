import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import '@fortawesome/fontawesome-free/js/all.js'
import Config from '@/shared/Config'

Vue.config.productionTip = false

async function loadConfig () {
  const configData = await window.Config.data()
  const config = new Config(configData)

  global.Sixpence = {
    config
  }
}

loadConfig().then(() => {
  new Vue({
    router,
    vuetify,
    render: h => h(App)
  }).$mount('#app')
})
