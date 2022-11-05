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
          v-for="(page, index) in menuMain"
          @click="goTo(page)"
          :key="index"
        >
          <v-list-item-action>
            <v-icon>{{ page.icon }}</v-icon>
          </v-list-item-action>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list dense>
        <v-list-item
          v-for="(page, index) in menuMisc"
          @click="goTo(page)"
          :key="index"
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
  },

  methods: {
    bindShortcutKeys: function () {
      const self = this

      Mousetrap.bind(['ctrl+shift+/', 'meta+shift+/'], () => {
        self.showAbout = true
        return false
      })
    },

    closeAbout: function () {
      this.showAbout = false
    },

    goTo: function (page) {
      this.pageName = page.name
      this.$router.push(page.path)
    }
  },

  data: () => ({
    drawer: true,
    showAbout: false,
    pageName: 'Home',
    menuMain: [
      { name: 'Home', path: '/', icon: 'mdi-home' }
    ],
    menuMisc: [
      { name: 'BlankSlate', path: '/blank', icon: 'fa-chalkboard' }
    ]
  })
}
</script>
