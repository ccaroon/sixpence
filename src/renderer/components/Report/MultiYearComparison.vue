<template>
  <div>
    <v-toolbar :color="constants.COLORS.TOOLBAR" dark dense app fixed>
      <v-menu bottom offset-y>
        <v-btn slot="activator" icon @click="handleBack()">
          <v-icon>mdi-arrow-left-thick</v-icon>
        </v-btn>
      </v-menu>
      <v-toolbar-title>Report - Income & Expenses By Year</v-toolbar-title>
      <v-toolbar-items>
      </v-toolbar-items>
    </v-toolbar>

    <template v-if="dataLoaded">
      <v-list dark dense fixed>
        <v-list-tile>
          <v-list-tile-avatar>
            <v-icon>mdi-cash</v-icon>
          </v-list-tile-avatar>
          <v-layout row>
            <v-flex xs3 align-self-center class="title">Category</v-flex>
            <v-flex align-self-center xs1 v-for="(year, id) in yearRange" :key="id">
              <v-btn @click="viewYear(year)">{{ year }}</v-btn>
            </v-flex>
          </v-layout>
        </v-list-tile>
      </v-list>

      <v-list dense>
        <v-list-tile
          v-for="(entry, category, id) in data"
          :class="entryColor(id, entry.type)"
          :key="id"
          @click="viewEntries(category)"
        >
          <v-list-tile-avatar>
            <v-icon>{{ entry.icon }}</v-icon>
          </v-list-tile-avatar>
          <v-layout row>
            <v-flex xs3>{{ category }}</v-flex>
            <v-flex text-xs-center xs1 v-for="(year, id) in yearRange" :key="id">
              <span v-if="entry[year]">{{ format.formatMoney(entry[year]) }}</span>
              <span v-else>N/A</span>
            </v-flex>
          </v-layout>
        </v-list-tile>
      </v-list>
    </template>
  </div>
</template>

<script>
import Constants from '../../lib/Constants'
import ExpenseDB from '../../lib/ExpenseDB'
import Format from '../../lib/Format'
import Moment from 'moment'

export default {
  name: 'MultiYearComparison',

  computed: {

  },

  mounted: function () {
    this.loadData()
  },

  methods: {
    entryColor: function (entryNum, type) {
      var color = null

      if (entryNum % 2 === 0) {
        color = (type === Constants.TYPE_INCOME) ? Constants.COLORS.INCOME : Constants.COLORS.EXPENSE
      } else {
        color = (type === Constants.TYPE_INCOME) ? Constants.COLORS.INCOME_ALT : Constants.COLORS.EXPENSE_ALT
      }

      return (color)
    },

    handleBack: function () {
      this.$router.push('/report/list')
    },

    viewYear: function (year) {
      this.$router.push(`/report/yearly-budget/${year}`)
    },

    viewEntries: function (category) {
      this.$router.push(`/expenses/category/${encodeURIComponent(category)}`)
    },

    loadData: function () {
      var self = this
      // NOTE: Load all data for now. May need to restrict this to X back years
      // for performance purposes later.
      var start = null
      var end = null

      ExpenseDB.search(start, end, {}, {type: 1, category: 1, date: 1, amount: 1})
        .then(function (entries) {
          entries.forEach(function (entry) {
            var category = entry.category
            var amount = entry.amount
            var year = Moment(entry.date).year()

            if (category !== Constants.ROLLOVER_CATEGORY) {
              if (year < self.minYear) {
                self.minYear = year
              }

              if (year > self.maxYear) {
                self.maxYear = year
              }

              if (!self.data[category]) {
                self.data[category] = {
                  icon: entry.icon,
                  type: entry.type
                }
              }

              if (!self.data[category][year]) {
                self.data[category][year] = 0.0
              }

              self.data[category][year] += amount
            }
          })

          for (var i = self.minYear; i <= self.maxYear; i++) {
            self.yearRange.push(i)
          }

          self.dataLoaded = true
        })
        .catch(function (err) {
          console.log(err)
        })
    }
  },

  data () {
    return ({
      minYear: 9999,
      maxYear: 0,
      yearRange: [],
      data: {},
      dataLoaded: false,
      format: Format,
      constants: Constants
    })
  }
}
</script>
