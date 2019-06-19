<template>
  <div>
    <v-toolbar :color="constants.COLORS.TOOLBAR" dark dense app fixed>
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

    <v-list dense>
      <v-list-tile
        v-for="(report, ri) in reportList"
        :key="ri"
        :class="rowColor(ri)"
        @click="viewReport(report)"
      >
        <v-list-tile-title>{{ report.title }}</v-list-tile-title>
        <v-list-tile-sub-title>{{ report.desc }}</v-list-tile-sub-title>
      </v-list-tile>
    </v-list>
  </div>
</template>

<script>
import Constants from '../../lib/Constants'

export default {
  name: 'Reports',
  components: {},

  mounted () {},

  computed: {},

  methods: {
    rowColor: function (index) {
      var color = index % 2 === 0 ? Constants.COLORS.GREY : Constants.COLORS.GREY_ALT
      return (color)
    },

    viewReport: function (report) {
      this.$router.push(report.url)
    }
  },

  data () {
    return {
      constants: Constants,
      reportList: [
        {
          title: 'Yearly Budget',
          url: '/report/yearly-budget',
          desc: 'Budget Progress for a Year'
        },
        {
          title: 'Multi-Year Income/Expense Comparison',
          url: '/report/multi-year-comparison',
          desc: 'Income & Expense Comparison between Years'
        }
      ]
    }
  }
}
</script>
