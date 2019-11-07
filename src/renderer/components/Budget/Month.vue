<template>
  <div>
    <v-list-item @click="budgetDetails()" :class="rowColor()" v-if="dataLoaded">
      <v-list-item-icon>
        <v-icon>{{ month.icon }}</v-icon>
      </v-list-item-icon>

      <v-row align="center">
        <v-col cols="3">
          <span class="subtitle-1">{{ month.text }}</span>
        </v-col>
        <v-col cols="3">
          <v-chip label :color="constants.COLORS.INCOME">
            <v-icon float-left>mdi-currency-usd</v-icon>
            <span class="subtitle-1">{{ format.formatMoney(monthData.income) }}</span>
          </v-chip>
        </v-col>
        <v-col cols="3">
          <v-chip label :color="constants.COLORS.EXPENSE">
            <v-icon float-left>mdi-currency-usd-off</v-icon>
            <span class="subtitle-1">{{ format.formatMoney(monthData.expense) }}</span>
          </v-chip>
        </v-col>
        <v-col cols="3">
          <v-chip
            label
            :color="monthData.diff >= 0.0 ? constants.COLORS.INCOME_ALT : constants.COLORS.EXPENSE_ALT"
          >
            <v-icon float-left>mdi-cash-multiple</v-icon>
            <span class="subtitle-1">{{ format.formatMoney(monthData.diff) }}</span>
            <v-icon :color="averageColor()" float-right>{{ averageIcon() }}</v-icon>
          </v-chip>
        </v-col>
      </v-row>
    </v-list-item>
  </div>
</template>

<script>
import BudgetDB from '../../lib/BudgetDB'
import Constants from '../../lib/Constants'
import Format from '../../lib/Format'
import Moment from 'moment'

const ICONS = {
  0: 'mdi-approval',
  1: 'mdi-arrow-up-bold',
  '-1': 'mdi-arrow-down-bold'
}

export default {
  name: 'BudgetMonth',

  props: ['month', 'average'],

  mounted () {
    var self = this
    var date = Moment().month(this.month.value - 1)
    BudgetDB.loadCategoryDataByMonth(date)
      .then(function (data) {
        self.monthData.income = 0.0
        self.monthData.expense = 0.0

        Object.values(data).forEach(function (amount) {
          if (amount >= 0.0) {
            self.monthData.income += amount
          } else {
            self.monthData.expense += amount
          }
        })

        self.monthData.diff = self.monthData.income + self.monthData.expense

        self.dataLoaded = true
      })
      .catch(function (err) {
        self.$emit('displayAlert', 'mdi-alert-octagon', 'red', err)
      })
  },

  // computed: {},

  methods: {
    budgetDetails: function () {
      this.$router.push({path: `/expenses/${this.month.value - 1}`})
    },

    rowColor: function () {
      var color = this.month.value % 2 === 0 ? Constants.COLORS.GREY : Constants.COLORS.GREY_ALT

      // Highlight Current Month
      if (this.month.value - 1 === (new Date()).getMonth()) {
        color = Constants.COLORS.ITEM_HIGHLIGHT
      }

      return (color)
    },

    averageIcon: function () {
      var i = ICONS[this.aboveBelowAverage()]
      return i
    },

    averageColor: function () {
      var color = 'black'
      if (this.aboveBelowAverage() === -1) {
        color = Constants.COLORS.EXPENSE
      } else if (this.aboveBelowAverage() === 1) {
        color = Constants.COLORS.INCOME
      }

      return (color)
    },

    // 0 == Equal; -1 == Below Avg; +1 == Above Agv
    aboveBelowAverage: function () {
      var aboveBelow = 0

      if (this.monthData.diff > this.average) {
        aboveBelow = +1
      } else if (this.monthData.diff < this.average) {
        aboveBelow = -1
      }

      return (aboveBelow)
    }
  },

  data () {
    return {
      constants: Constants,
      format: Format,
      dataLoaded: false,
      monthData: {}
    }
  }
}
</script>
