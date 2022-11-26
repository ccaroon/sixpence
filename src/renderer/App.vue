<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      app
      dark
      mini-variant
      mobile-breakpoint="640"
    >
      <v-list dense>
        <v-list-item
          v-for="(page, name) in menuMain"
          @click="goTo(name)"
          :key="name"
        >
          <v-list-item-action>
            <v-icon>{{ page.icon }}</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list dense>
        <v-list-item
          v-for="(page, name) in menuMisc"
          @click="goTo(name)"
          :key="name"
        >
          <v-list-item-action>
            <v-icon>{{ page.icon }}</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <About v-model="showAbout" v-on:close="closeAbout" />
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import About from './components/About'
import Mousetrap from 'mousetrap'

export default {
  name: 'DaikonApp',
  components: { About },
  mounted () {
    this.bindShortcutKeys()
    this.registerMenuHandlers()
  },

  methods: {
    bindShortcutKeys: function () {
      const self = this

      Mousetrap.bind(['ctrl+shift+/', 'meta+shift+/'], () => {
        self.showAbout = true
        return false
      })
    },

    registerMenuHandlers: function () {
      // View
      window.Menu.registerHandler('menu-view-main', (event) => {
        this.goTo('Main')
      })

      window.Menu.registerHandler('menu-view-budget', (event) => {
        this.goTo('Budget')
      })

      window.Menu.registerHandler('menu-view-expenses', (event) => {
        this.goTo('Expenses')
      })

      window.Menu.registerHandler('menu-view-reports', (event) => {
        this.goTo('Reports')
      })

      // Help
      window.Menu.registerHandler('menu-help-about', (event) => {
        this.showAbout = true
      })
    },

    closeAbout: function () {
      this.showAbout = false
    },

    goTo: function (pageName) {
      this.$router.push({ name: pageName, params: { } })
    }
  },

  data: () => ({
    drawer: true,
    showAbout: false,
    menuMain: {
      Main: { icon: 'fa-house' },
      Budget: { icon: 'fa-money-bill-trend-up' },
      Expenses: { icon: 'fa-money-bill-transfer' },
      Reports: { icon: 'fa-chart-simple' }
    },
    menuMisc: {}
  })
}
</script>
