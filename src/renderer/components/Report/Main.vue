<template>
<div>
  <v-toolbar color="grey darken-2" dark dense app fixed>
    <v-menu bottom offset-y>
      <v-btn slot="activator" icon>
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-list dense>
        <v-list-tile v-for="(report,i) in reports" :key="i" @click="viewReport(report)">
          <v-list-tile-title>{{ report.title }}</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-menu>
    <v-toolbar-title>Reports - {{ activeReport.title || '' }}</v-toolbar-title>
  </v-toolbar>

   <template v-if="activeReport.action == 'listReports' && activeReport.visible">
     <v-list dense v-for="(report, ri) in reportData" :key="ri">
       <v-list-tile @click="viewReport(report)">
         <v-list-tile-title >{{ report.title }}</v-list-tile-title>
       </v-list-tile>
     </v-list>
   </template>

  <template v-if="activeReport.action == 'yearlySpending' && activeReport.visible">
    <v-list dense v-for="entry in reportData" :key="entry._id">
      <ExpenseEntry
        v-bind:entry="entry">
      </ExpenseEntry>
    </v-list>
  </template>

  <template v-if="activeReport.action == 'catByYear' && activeReport.visible">
    <v-list dense v-for="(entry, id) in reportData" :key="id">
      <ExpenseCategory
        v-bind:entry="entry">
      </ExpenseCategory>
    </v-list>
  </template>
</div>
</template>

<script>
import BudgetDB from '../../lib/BudgetDB'
// import Constants from '../lib/Constants'
import ExpenseEntry from '../Expense/Entry'
import ExpenseCategory from '../Expense/Category'
import ExpenseDB from '../../lib/ExpenseDB'
// import Format from '../lib/Format'
// import Icons from '../lib/Icons'
// import Mousetrap from 'mousetrap'
import Moment from 'moment'

export default {
  name: 'Reports',
  components: { ExpenseEntry, ExpenseCategory },

  mounted () {
    this.viewReport(this.reports[0])
  },

  computed: {
  },

  methods: {
    listReports: function () {
      this.reportData = this.reports.slice(1)
      this.activeReport.visible = true
    },

    yearlySpending: function () {
      var self = this
      var year = Moment().year()

      ExpenseDB.loadData(Moment(`${year}-01-01`).toDate(), Moment(`${year}-12-31`).toDate())
        .then(function (data) {
          self.reportData = data
          self.activeReport.visible = true
        })
        .catch(function (err) {
          console.log(err)
        })
    },

    catByYear: function () {
      var self = this
      var year = Moment().year()
      var groupedData = {}

      BudgetDB.loadData()
        .then(function (categories) {
          // Seed Budgeted Categories
          categories.forEach(function (cat) {
            groupedData[cat.category] = {
              type: cat.type,
              icon: cat.icon,
              category: cat.category,
              amount: 0.0,
              budgetedAmount: cat.amount * (12 / cat.frequency)
            }
          })

          return ExpenseDB.loadData(Moment(`${year}-01-01`).toDate(), Moment(`${year}-12-31`).toDate())
        })
        .then(function (entries) {
          entries.forEach(function (entry) {
            if (groupedData.hasOwnProperty(entry.category)) {
              groupedData[entry.category].amount += entry.amount
            }
          })

          self.reportData = Object.values(groupedData)
          self.activeReport.visible = true
        })
        .catch(function (err) {
          console.log(err)
        })
    },

    // Report Router
    viewReport: function (report) {
      this.reports.forEach(r => { r.visible = false })

      this.activeReport = report
      this[report.action]()
    }
  },

  watch: {},

  data () {
    var reportMenu = [
      {
        title: 'Report List',
        action: 'listReports',
        visible: false
      },
      {
        title: 'Yearly Spending',
        action: 'yearlySpending',
        visible: false
      },
      {
        title: 'Year By Category',
        action: 'catByYear',
        visible: false
      }
    ]

    return {
      reports: reportMenu,
      activeReport: reportMenu[0],
      reportData: null
    }
  }
}
</script>
