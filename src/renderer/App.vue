<template>
  <v-app id="app">
    <v-content container--fluid>
      <About></About>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import About from './components/About'
import BudgetDB from './lib/BudgetDB'
import ExpenseDB from './lib/ExpenseDB'

const { ipcRenderer } = require('electron')

export default {
  name: 'Sixpence',
  components: { About },

  mounted () {
    ipcRenderer.on('menu-view-main', (event, arg) => {
      this.$router.push('/')
    })

    ipcRenderer.on('menu-view-budget', (event, arg) => {
      this.$router.push('/budget')
    })

    ipcRenderer.on('menu-view-expenses', (event, arg) => {
      this.$router.push('/expenses')
    })

    ipcRenderer.on('menu-view-reports', (event, arg) => {
      this.$router.push('/report/list')
    })

    ipcRenderer.on('menu-settings', (event, arg) => {
      this.$router.push('/settings')
    })

    ipcRenderer.on('sixpence-renderer-cleanup', (event, msg) => {
      this.cleanup(msg)
        .then((values) => {
          ipcRenderer.send('sixpence-main-cleanup', 0, msg)
        })
        .catch((error) => {
          console.log(error)
        })
    })
  },

  methods: {
    cleanup: function (msg) {
      // ---------------------------------------------------
      // var doNothing = new Promise((resolve, reject) => {
      //   resolve(true)
      // })
      // return Promise.all([doNothing])
      // ---------------------------------------------------

      const compactBDB = new Promise((resolve, reject) => {
        BudgetDB.compact(() => {
          resolve(true)
        })
      })

      const compactEDB = new Promise((resolve, reject) => {
        ExpenseDB.compact(() => {
          resolve(true)
        })
      })

      return Promise.all([compactBDB, compactEDB])
    }
  }

}
</script>
