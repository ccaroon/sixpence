<template>
<div>
  <v-toolbar color="grey darken-2" dark dense app fixed>
    <v-menu bottom offset-y>
      <v-btn slot="activator" icon @click="handleBack()">
        <v-icon>mdi-arrow-left-thick</v-icon>
      </v-btn>
    </v-menu>
    <v-toolbar-title v-if="view === 'catByYear'">Report - All Budgeted Categories - {{ this.year }}</v-toolbar-title>
    <v-toolbar-title v-if="view === 'catByMonth' && dataLoaded">
      Report - Category by Month
      <v-chip class="subheading" color="orange lighten-2" label disabled>
        {{ selectedCategory }} 
      </v-chip>
      <v-chip class="subheading" color="grey lighten-1" label disabled>
        {{ this.year }}
      </v-chip>
      <v-chip :color="amountColor(reportData.totalSpent,3)" text-color="black" tabindex="-1" disabled>
        <v-icon left>fa-calendar</v-icon>
        <span class="subheading">{{ format.formatMoney(Math.abs(reportData.totalSpent)) }}</span>
      </v-chip>
      <v-chip :color="amountColor(reportData.avgSpent)" text-color="black" tabindex="-1" disabled>
        <v-icon left>mdi-cash-multiple</v-icon>
        <span class="subheading">{{ format.formatMoney(Math.abs(reportData.avgSpent)) }} / Month</span>
      </v-chip>
    </v-toolbar-title>
  </v-toolbar>

  <template v-if="view === 'catByMonth' && dataLoaded">
    <v-list dense v-for="month in constants.MONTHS" :key="month.value">
      <YearlyCatByMonth
        v-bind:month="month"
        v-bind:data="reportData.data[month.value]">
      </YearlyCatByMonth>
    </v-list>
  </template>
  
  <template v-else-if="view === 'catByYear' && dataLoaded">
    <v-list dense v-for="(entry, id) in reportData" :key="id">
      <ExpenseCategory
        v-bind:entry="entry"
        v-on:viewEntriesInGroup="viewCategoryByMonth">
      </ExpenseCategory>
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
  name: 'ReportYearly',
  components: { ExpenseCategory, YearlyCatByMonth },

  mounted () {
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

      BudgetDB.loadData()
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
      this.reportData = {
        'totalSpent': totalSpent,
        'avgSpent': totalSpent / 12.0,
        'data': []
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
