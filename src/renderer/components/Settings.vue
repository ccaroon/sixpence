<template>
  <div>
    <v-tabs
      grow
      :color="constants.COLORS.TOOLBAR_BUTTON"
      :background-color="constants.COLORS.TOOLBAR"
      v-model="tab"
      dark
    >
      <v-tab v-for="(_, group, index) in settings" :key="index">{{group}}</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item v-for="(options, group, index) in settings" :key="index">
        <SettingsOption v-bind:options="options" v-bind:metadata="metadata[group]"></SettingsOption>
      </v-tab-item>
    </v-tabs-items>

    <v-btn bottom right fixed fab :color="constants.COLORS.OK_BUTTON" @click="save()">Save</v-btn>
  </div>
</template>
<script>
import Constants from '../lib/Constants'
import SettingsOption from './Settings/Option'
import Config from '../../main/config'
Config.load()

export default {
  name: 'Settings',
  components: { SettingsOption },

  mounted () {
  },

  methods: {
    save: function () {
      Config.save()
      alert('Saved')
    }
  },

  data () {
    return {
      tab: null,
      metadata: Config.metaData,
      constants: Constants,
      settings: Config.get()
    }
  }
}
</script>
