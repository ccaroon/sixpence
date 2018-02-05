<template>
  <v-data-table
    :items="items">
    <template slot="items" slot-scope="data">
      <td>{{ data.item.name }}</td>
      <td>{{ data.item.value }}</td>
    </template>
  </v-data-table>
</template>

<script>
  export default {
    data () {
      return {
        items: [
          { name: 'Electron Version', value: process.versions['atom-shell'] },
          { name: 'Route', value: this.$route.name },
          { name: 'NodeJS Version', value: process.versions.node },
          { name: 'Path', value: this.$route.path },
          { name: 'Platform', value: require('os').platform() },
          { name: 'Vue Version', value: require('vue/package.json').version }
        ]

      }
    }
  }
</script>
