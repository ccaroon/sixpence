<template>
  <v-container>
    <v-row dense no-gutters v-for="(value, name, index) in options" :key="index">
      <v-col>
        <v-file-input
          v-if="metadata[name].type === 'FILE'"
          webkitdirectory
          :label="metadata[name].desc"
          truncate-length="80"
          outlined
          :prepend-icon="metadata[name].icon"
          :clearable="false"
          v-model="files[name]"
        ></v-file-input>
        <v-text-field
          v-else
          :type="metadata[name].type"
          :label="metadata[name].desc"
          :placeholder="value.toString()"
          outlined
          :prepend-icon="metadata[name].icon"
          :key="index"
          v-model="options[name]"
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  name: 'SettingsOption',

  props: ['options', 'metadata'],

  methods: {
    updateFileOptions: function () {
      for (const [name, file] of Object.entries(this.files)) {
        if (file && file.path) {
          this.options[name] = file.path
        }
      }
    }

  },

  watch: {
    files: {
      handler: 'updateFileOptions',
      deep: true
    }
  },

  data () {
    const files = {}
    for (const [name, mdata] of Object.entries(this.metadata)) {
      if (mdata.type === 'FILE') {
        files[name] = new File([], this.options[name])
      }
    }

    return {
      files: files
    }
  }
}
</script>
