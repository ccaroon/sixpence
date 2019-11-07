<template>
  <div>
    <v-app-bar :color="constants.COLORS.TOOLBAR" dark dense app fixed>
      <v-menu bottom offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon @click="handleBack()">
            <v-icon>mdi-arrow-left-thick</v-icon>
          </v-btn>
        </template>
      </v-menu>
      <v-toolbar-title>Report - Income & Expenses By Year</v-toolbar-title>
    </v-app-bar>

    <template v-if="dataLoaded">
      <v-list dense dark>
        <v-list-item>
          <v-list-item-icon>
            <v-icon>{{ focusData.data.icon ? focusData.data.icon : 'mdi-all-inclusive'}}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-row no-gutters align="center">
              <v-col cols="3">{{ focusData.category ? focusData.category : 'Category'}}</v-col>
              <v-col cols="1" text-center v-for="(year, id) in yearRange" :key="id">
                <v-btn small @click="viewYear(year)">{{ year }}</v-btn>
              </v-col>
            </v-row>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <!-- All Categories -->
      <v-list dense v-show="!focusData.category">
        <v-list-item
          v-for="(entry, category, id) in data"
          :class="entryColor(id, entry.type)"
          :key="id"
        >
          <v-list-item-icon>
            <v-icon>{{ entry.icon }}</v-icon>
          </v-list-item-icon>

          <v-row dense align="center">
            <v-col cols="3">{{ category }}</v-col>

            <v-col cols="1" v-for="(year, id) in yearRange" :key="id">
              <span v-if="entry[year]">{{ format.formatMoney(entry[year]['total']) }}</span>
              <span v-else>N/A</span>
            </v-col>

            <!-- ACTIONS : Offset to align right -->
            <!-- grid size - ICON - CATEGORY - 1/year amount -->
            <v-col :offset="12 - 1 - 3 - (yearRange.length)">
              <v-btn icon @click="viewEntries(category)">
                <v-icon>mdi-view-list</v-icon>
              </v-btn>

              <v-btn icon @click="focusSingleCategory(category)">
                <v-icon>mdi-image-filter-center-focus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-list-item>
      </v-list>

      <!-- Focus on Single Category -->
      <v-list v-show="focusData.category">
        <v-list-item
          v-for="month in constants.MONTHS"
          :key="month.value"
          :class="month.value % 2 === 0 ? constants.COLORS.GREY : constants.COLORS.GREY_ALT"
        >
          <v-list-item-icon>
            <v-icon>{{ month.icon }}</v-icon>
          </v-list-item-icon>

          <v-row dense align="center">
            <v-col cols="3">
              <span class="subtitle-1">{{ month.text }}</span>
            </v-col>
            <v-col cols="1" v-for="(year, id) in yearRange" :key="id">
              <span
                v-if="focusData.data[year]"
              >{{ format.formatMoney(focusData.data[year]['months'][month.value-1]) }}</span>
              <span v-else>N/A</span>
            </v-col>
          </v-row>
        </v-list-item>
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
      if (this.focusData.category) {
        this.clearFocus()
      } else {
        this.$router.push('/report/list')
      }
    },

    viewYear: function (year) {
      this.$router.push(`/report/yearly-budget/${year}`)
    },

    viewEntries: function (category) {
      this.$router.push(`/expenses/category/${encodeURIComponent(category)}`)
    },

    clearFocus: function () {
      this.focusData = {category: null, data: {}}
    },

    focusSingleCategory: function (category) {
      this.focusData = {
        category: category,
        data: this.data[category]
      }
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
            var month = Moment(entry.date).month()
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
                self.data[category][year] = {
                  months: new Array(12).fill(0.0),
                  total: 0.0
                }
              }

              self.data[category][year]['months'][month] += amount
              self.data[category][year]['total'] += amount
            }
          })

          // TODO: don't allow anymore than yearCount years into yearRange
          for (var i = self.minYear; i <= self.maxYear; i++) {
            self.yearRange.push(i)
          }

          // console.log(self.data)

          self.dataLoaded = true
        })
        .catch(function (err) {
          console.log(err)
        })
    }
  },

  data () {
    return ({
      yearCount: 5, // Number of years to display - not used yet
      minYear: 9999,
      maxYear: 0,
      yearRange: [],
      focusData: {category: null, data: {}},
      data: {},
      dataLoaded: false,
      format: Format,
      constants: Constants
    })
  }
}
</script>
