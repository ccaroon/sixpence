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
      <template v-if="view === 'catByYear'">
        <v-toolbar-title>Report - Budget Progress for {{ this.year }}</v-toolbar-title>
      </template>
      <template v-if="view === 'catByMonth' && dataLoaded">
        <v-toolbar-title>Report - {{ selectedCategory }} for {{ this.year }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-row no-gutters>
          <v-col>
            <v-toolbar-items>
              <v-chip :color="amountColor(reportData.totalSpent,3)" text-color="black">
                <v-icon float-left>fa-calendar</v-icon>
                <span class="subtitle-1">{{ format.formatMoney(Math.abs(reportData.totalSpent)) }}</span>
              </v-chip>&nbsp;
              <v-chip :color="amountColor(reportData.avgSpent)" text-color="black">
                <v-icon float-left>mdi-cash-multiple</v-icon>
                <span
                  class="subtitle-1"
                >{{ format.formatMoney(Math.abs(reportData.avgSpent)) }} / Month</span>
              </v-chip>
            </v-toolbar-items>
          </v-col>
        </v-row>
      </template>
      <v-spacer></v-spacer>
    </v-app-bar>

    <template v-if="view === 'catByMonth' && dataLoaded">
      <v-list dense>
        <YearlyCatByMonth
          v-for="month in constants.MONTHS"
          :key="month.value"
          v-bind:month="month"
          v-bind:data="reportData.data[month.value]"
        ></YearlyCatByMonth>
      </v-list>
    </template>

    <template v-else-if="view === 'catByYear' && dataLoaded">
      <v-list dense>
        <ExpenseCategory
          v-for="(entry, id) in reportData"
          :key="id"
          v-bind:entry="entry"
          v-on:viewEntriesInGroup="viewCategoryByMonth"
        ></ExpenseCategory>
      </v-list>
    </template>
  </div>
</template>
<script>
import BudgetDB from '../../lib/BudgetDB'
import Constants from '../../lib/Constants'
import ExpenseCategory from '../Expense/Category'
import ExpenseDB from '../../lib/ExpenseDB'
import Format from '../../lib/Format'
import YearlyCatByMonth from './YearlyCatByMonth'
import Moment from 'moment'

export default {
  name: 'YearlyBudget',
  components: { ExpenseCategory, YearlyCatByMonth },

  mounted () {
    if (this.$route.params.year) {
      this.year = this.$route.params.year
      this.yearStart = Moment(`${this.year}-01-01`).toDate()
      this.yearEnd = Moment(`${this.year}-12-31`).toDate()
    }

    this.viewCategoryByYear()
  },

  computed: {},

  methods: {

    amountColor: function (amount, accent = 1) {
      var color = ''

      if (amount >= 0.0) {
        color = 'green accent-' + accent
      } else {
        color = 'red accent-' + accent
      }
      return (color)
    },

    handleBack: function () {
      if (this.view === 'catByYear') {
        this.$router.push('/report/list')
      } else {
        this.viewCategoryByYear()
      }
    },

    viewCategoryByYear: function () {
      var self = this
      var groupedData = {}

      this.view = 'catByYear'
      this.dataLoaded = false

      BudgetDB.getEntries(BudgetDB.QUERIES.ACTIVE_AFTER(this.yearStart))
        .then(function (categories) {
          // Seed Budgeted Categories
          categories.forEach(function (cat) {
            if (groupedData.hasOwnProperty(cat.category)) {
              groupedData[cat.category]['budgetedAmount'] += cat.amount * (12 / cat.frequency)
            } else {
              groupedData[cat.category] = {
                type: cat.type,
                icon: cat.icon,
                category: cat.category,
                amount: 0.0,
                budgetedAmount: cat.amount * (12 / cat.frequency)
              }
            }
          })

          return ExpenseDB.loadData(self.yearStart, self.yearEnd)
        })
        .then(function (entries) {
          entries.forEach(function (entry) {
            if (groupedData.hasOwnProperty(entry.category)) {
              groupedData[entry.category].amount += entry.amount
            }
          })

          self.reportData = Object.values(groupedData)
          self.dataLoaded = true
        })
        .catch(function (err) {
          console.log(err)
        })
    },

    viewCategoryByMonth: function (catName, totalSpent) {
      var self = this

      this.selectedCategory = catName
      this.view = 'catByMonth'
      this.dataLoaded = false

      // If viewing the current year, only average up to the current month,
      // otherwise average across a full year (12 months)
      var now = Moment()
      var divisor = this.year === now.year() ? now.month() + 1 : 12.0

      this.reportData = {
        totalSpent: totalSpent,
        avgSpent: totalSpent / divisor,
        data: []
      }

      BudgetDB.search({'category': catName})
        .then(function (cats) {
          self.constants.MONTHS.forEach(function (month) {
            var monthStart = Moment(`${self.year}-${month.value}`, 'YYYY-M', true).startOf('month').toDate()
            var monthEnd = Moment(`${self.year}-${month.value}`, 'YYYY-M', true).endOf('month').toDate()

            self.reportData.data[month.value] = {'amount': 0.0, 'budgetedAmount': 0.0}

            ExpenseDB.search(monthStart, monthEnd, {'category': catName})
              .then(function (entries) {
                cats.forEach(function (category) {
                  if (BudgetDB.isDue(month.value, category.frequency, category.firstDue)) {
                    self.reportData.data[month.value]['budgetedAmount'] += category.amount
                  }
                })

                entries.forEach(function (entry) {
                  self.reportData.data[month.value]['amount'] += entry.amount
                })

                if (month.value === 12) {
                  self.dataLoaded = true
                }
              })
              .catch(function (err) {
                console.log(err)
              })
          })
        })
        .catch(function (err) {
          console.log(err)
        })
    }
  },

  data () {
    var thisYear = Moment().year()
    var yearStart = Moment(`${thisYear}-01-01`).toDate()
    var yearEnd = Moment(`${thisYear}-12-31`).toDate()

    return {
      constants: Constants,
      format: Format,
      view: 'catByYear',
      year: thisYear,
      yearStart: yearStart,
      yearEnd: yearEnd,
      selectedCategory: null,
      reportData: null,
      dataLoaded: false
    }
  }
}
</script>
