<template>
  <v-app id="app">
    <v-content fluid>
      <About></About>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import About from './components/About'

const {ipcRenderer} = require('electron')

export default {
  name: 'Sixpence',
  components: { About },

  mounted () {
    ipcRenderer.on('menu-view-main', (event, arg) => {
      this.$router.push(`/`)
    })

    ipcRenderer.on('menu-view-budget', (event, arg) => {
      this.$router.push(`/budget`)
    })

    ipcRenderer.on('menu-view-expenses', (event, arg) => {
      this.$router.push(`/expenses`)
    })
  }

}
</script>
