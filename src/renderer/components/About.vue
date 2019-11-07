<template>
  <v-dialog v-model="showDialog" max-width="768">
    <v-card>
      <v-card-title id="about-title" class="headline green lighten-1">
        <img width="64" src="../assets/logo.png" />
        &nbsp;
        {{ appInfo.name }} v{{ appInfo.version }}
      </v-card-title>
      <v-card-text>
        {{ appInfo.description }} &mdash; &copy; {{ appInfo.author }} 2018-{{ new Date().getFullYear() }}
        <v-divider></v-divider>
        <v-subheader>Built With</v-subheader>
        <v-data-table :items="items" hide-default-footer hide-default-header dark>
          <template v-slot:body="{ items }">
            <tbody>
              <tr v-for="item in items" :key="item.name">
                <td>
                  <v-icon>mdi-{{ item.icon }}</v-icon>
                  {{ item.name }}
                </td>
                <td :id="'about-tech-' + item.name.toLowerCase().replace(' ', '')">{{ item.value }}</td>
              </tr>
            </tbody>
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
      var data = {
        showDialog: false,
        appInfo: pkgJson,
        items: [
          { name: 'Electron', value: process.versions.electron, icon: 'atom' },
          { name: 'NodeJS', value: process.versions.node, icon: 'nodejs' },
          { name: 'Chrome', value: process.versions.chrome, icon: 'google-chrome' },
          { name: 'Platform', value: require('os').platform(), icon: 'laptop' },
          { name: 'Vue Version', value: require('vue/package.json').version, icon: 'vuejs' }
        ]
      }

      if (process.platform === 'darwin') {
        data.items[3].icon = 'apple'
      } else if (process.platform === 'win32') {
        data.items[3].icon = 'windows'
      } else if (process.platform === 'linux') {
        data.items[3].icon = 'linux'
      }

      return (data)
    }
  }
</script>
