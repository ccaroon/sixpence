<template>
  <div>
    <v-app-bar :color="constants.COLORS.TOOLBAR" dark dense app fixed>
      <v-menu bottom offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon>
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>

        <v-list dense>
          <v-list-item v-for="(report, ri) in reportList" :key="ri" @click="viewReport(report)">
            <v-list-item-title>{{ report.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-toolbar-title>Report List</v-toolbar-title>
    </v-app-bar>

    <v-list dense>
      <v-list-item
        v-for="(report, ri) in reportList"
        :key="ri"
        :class="rowColor(ri)"
        @click="viewReport(report)"
      >
        <v-list-item-icon>
          <v-icon>{{ report.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="body-1">{{ report.title }}</v-list-item-title>
          <v-list-item-subtitle>{{ report.desc }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
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
          icon: 'mdi-calendar-star',
          title: 'Yearly Budget',
          url: '/report/yearly-budget',
          desc: 'Budget progress for the current year'
        },
        {
          icon: 'mdi-compare',
          title: 'Multi-Year Income/Expense Comparison',
          url: '/report/multi-year-comparison',
          desc: 'Income & Expense comparison between years'
        }
      ]
    }
  }
}
</script>
