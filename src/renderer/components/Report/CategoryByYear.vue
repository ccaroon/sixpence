<template>
  <div>
    <v-toolbar color="grey darken-2" dark dense app fixed>
      <v-menu bottom offset-y>
        <v-btn slot="activator" icon @click="handleBack()">
          <v-icon>mdi-arrow-left-thick</v-icon>
        </v-btn>
      </v-menu>
      <v-toolbar-title>Report - Category By Year</v-toolbar-title>
    </v-toolbar>

    <template v-if="dataLoaded">
      <v-list dark dense fixed>
        <v-list-tile>
          <v-list-tile-avatar>
            <v-icon>mdi-cash</v-icon>
          </v-list-tile-avatar>
          <v-layout row>
            <v-flex xs3 class="title">Category</v-flex>
            <v-flex xs1 class="title" v-for="(year, id) in yearRange" :key="id">{{ year }}</v-flex>
          </v-layout>
        </v-list-tile>
      </v-list>

      <v-list dense>
        <v-list-tile
          :class="entryColor(entry.type)"
          v-for="(entry, category, id) in data"
          :key="id"
          @click="function(){}"
        >
          <v-list-tile-avatar>
            <v-icon>{{ entry.icon }}</v-icon>
          </v-list-tile-avatar>
          <v-layout row>
            <v-flex xs3>{{ category }}</v-flex>
            <v-flex xs1 v-for="(year, id) in yearRange" :key="id">
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
  name: 'CategoryByYear',

  computed: {

  },

  mounted: function () {
    this.loadData()
  },

  methods: {
    entryColor: function (type) {
      var color = type === Constants.TYPE_INCOME ? 'green accent-1' : 'red accent-1'
      return (color)
    },

    handleBack: function () {
      this.$router.push('/report/list')
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
      format: Format
    })
  }
}
</script>
