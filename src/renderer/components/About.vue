<template>
  <v-dialog v-model="showDialog" max-width="768">
    <v-card>
      <v-card-title class="headline green lighten-1">
        <img width="64" src="../assets/logo.png"></img>&nbsp;
        {{ appInfo.name }} v{{ appInfo.version }}
      </v-card-title>
      <v-card-text>
        {{ appInfo.description }}
        <v-divider></v-divider>
        <v-subheader>Built With</v-subheader>
        <v-data-table :items="items" hide-actions hide-headers dark>
          <template slot="items" slot-scope="data">
            <td>{{ data.item.name }}</td>
            <td>{{ data.item.value }}</td>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
  const {ipcRenderer} = require('electron')
  const pkgJson = require(`../../../package.json`)

  export default {
    mounted () {
      ipcRenderer.on('menu-help-about', (event, arg) => {
        this.showDialog = true
      })
    },

    data () {
      return {
        showDialog: false,
        appInfo: pkgJson,
        items: [
          { name: 'Electron', value: process.versions['atom-shell'] },
          // { name: 'Route', value: this.$route.name },
          { name: 'NodeJS', value: process.versions.node },
          // { name: 'Path', value: this.$route.path },
          { name: 'Platform', value: require('os').platform() },
          { name: 'Vue Version', value: require('vue/package.json').version }
        ]
      }
    }
  }
</script>
