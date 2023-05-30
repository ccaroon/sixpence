<template>
  <div>
    <v-tabs
      grow
      :color="constants.COLORS.TOOLBAR_BUTTON"
      :background-color="constants.COLORS.TOOLBAR"
      v-model="tab"
      dark
    >
      <v-tab v-for="(_, group, index) in settings" :key="index">{{
        group
      }}</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item v-for="(options, group, index) in settings" :key="index">
        <SettingsOption
          v-bind:options="options"
          v-bind:metadata="metadata[group]"
        ></SettingsOption>
      </v-tab-item>
    </v-tabs-items>

    <v-btn
      bottom
      right
      fixed
      fab
      :color="constants.COLORS.OK_BUTTON"
      @click="save()"
      >Save</v-btn
    >
  </div>
</template>
<script>
import Constants from '../lib/Constants'
import SettingsOption from './Settings/Option'

export default {
  name: 'settings-main',
  components: { SettingsOption },

  mounted () {
  },

  methods: {
    save: function () {
      alert('Not Yet Implemented!')
    }
  },

  data () {
    return {
      tab: null,
      metadata: global.Sixpence.config.metaData,
      constants: Constants,
      settings: global.Sixpence.config.data
    }
  }
}
</script>
