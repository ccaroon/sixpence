<template>
  <div>
    <v-toolbar color="grey darken-2" dark dense app fixed>
      <v-menu bottom offset-y>
        <v-btn slot="activator" icon>
          <v-icon>mdi-menu</v-icon>
        </v-btn>
        <v-list dense>
          <v-list-tile v-for="(report, ri) in reportList" :key="ri" @click="viewReport(report)">
            <v-list-tile-title>{{ report.title }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
      <v-toolbar-title>Report List</v-toolbar-title>
    </v-toolbar>

    <v-list dense v-for="(report, ri) in reportList" :key="ri">
      <v-list-tile @click="viewReport(report)">
        <v-list-tile-title>{{ report.title }}</v-list-tile-title>
        <v-list-tile-sub-title>{{ report.desc }}</v-list-tile-sub-title>
      </v-list-tile>
    </v-list>
  </div>
</template>

<script>
export default {
  name: 'Reports',
  components: {},

  mounted () {},

  computed: {},

  methods: {
    viewReport: function (report) {
      this.$router.push(report.url)
    }
  },

  data () {
    return {
      reportList: [
        {
          title: 'Year By Category',
          url: '/report/yearly',
          desc: 'Summary of Income/Expenses by Category for an entire Year'
        },
        {
          title: 'Category Across Years',
          url: '/report/category_by_year',
          desc: 'Year by Year Comparison of each Category'
        }
      ]
    }
  }
}
</script>
