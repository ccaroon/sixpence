<template>
  <div>
    <v-toolbar :color="constants.COLORS.TOOLBAR" dark dense app fixed>
      <v-menu bottom offset-y>
        <v-btn slot="activator" icon @click="handleBack()">
          <v-icon>mdi-arrow-left-thick</v-icon>
        </v-btn>
      </v-menu>
      <v-toolbar-title>Report - Income & Expenses By Year</v-toolbar-title>
    </v-toolbar>

    <template v-if="dataLoaded">
      <v-list dark dense fixed>
        <v-list-tile>
          <v-list-tile-avatar>
            <v-icon>{{ focusData.data.icon ? focusData.data.icon : 'mdi-all-inclusive'}}</v-icon>
          </v-list-tile-avatar>
          <v-layout row>
            <v-flex
              xs3
              align-self-center
              class="title"
            >{{ focusData.category ? focusData.category : 'Category'}}</v-flex>
            <v-flex align-self-center xs1 v-for="(year, id) in yearRange" :key="id">
              <v-btn @click="viewYear(year)">{{ year }}</v-btn>
            </v-flex>
          </v-layout>
        </v-list-tile>
      </v-list>

      <!-- All Categories -->
      <v-list dense v-show="!focusData.category">
        <v-list-tile
          v-for="(entry, category, id) in data"
          :class="entryColor(id, entry.type)"
          :key="id"
          @click
        >
          <v-list-tile-avatar>
            <v-icon>{{ entry.icon }}</v-icon>
          </v-list-tile-avatar>
          <v-layout row align-center>
            <v-flex xs3>
              <span class="subheading">{{ category }}</span>
            </v-flex>
            <v-flex text-xs-center xs1 v-for="(year, id) in yearRange" :key="id">
              <span v-if="entry[year]">{{ format.formatMoney(entry[year]['total']) }}</span>
              <span v-else>N/A</span>
            </v-flex>
            <v-flex xs offset-xs5>
              <v-list-tile-action>
                <v-btn flat icon @click="viewEntries(category)">
                  <v-icon>mdi-view-list</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-flex>
            <v-flex xs1>
              <v-list-tile-action>
                <v-btn flat icon @click="focusSingleCategory(category)">
                  <v-icon>mdi-image-filter-center-focus</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-flex>
          </v-layout>
        </v-list-tile>
      </v-list>

      <!-- Focus on Single Category -->
      <v-list v-show="focusData.category">
        <v-list-tile
          v-for="month in constants.MONTHS"
          :key="month.value"
          :class="month.value % 2 === 0 ? constants.COLORS.GREY : constants.COLORS.GREY_ALT"
        >
          <v-list-tile-avatar>
            <v-icon>{{ month.icon }}</v-icon>
          </v-list-tile-avatar>
          <v-layout row align-center>
            <v-flex xs3>
              <span class="subheading">{{ month.text }}</span>
            </v-flex>
            <v-flex text-xs-center xs1 v-for="(year, id) in yearRange" :key="id">
              <span
                v-if="focusData.data[year]"
              >{{ format.formatMoney(focusData.data[year]['months'][month.value-1]) }}</span>
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
