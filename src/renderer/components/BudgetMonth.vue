<template>
<div>

  <v-list-tile @click="budgetDetails()" :class="month.value % 2 === 0 ? 'grey lighten-4' : 'grey lighten-2'" v-if="dataLoaded">
    <v-list-tile-avatar>
      <v-icon>{{ month.icon }}</v-icon>
    </v-list-tile-avatar>
    <v-layout row>
      <v-flex xs3><v-avatar class="subheading">{{ month.text }}</v-avatar></v-flex>
      <v-flex xs3>
        <v-chip color="green accent-1">
          <v-icon left>mdi-currency-usd</v-icon>
          <span class="subheading">{{ format.formatMoney(monthData.income) }}</span>
        </v-chip>
      </v-flex>
      <v-flex xs3>
        <v-chip color="red accent-1">
          <v-icon left>mdi-currency-usd-off</v-icon>
          <span class="subheading">{{ format.formatMoney(monthData.expense) }}</span>
        </v-chip>
      </v-flex>
      <v-flex xs3>
        <v-chip :color="monthData.diff >= 0.0 ? 'green accent-3' : 'red accent-3'">
            <v-icon left>mdi-cash-multiple</v-icon>
            <span class="subheading">{{ format.formatMoney(monthData.diff) }}</span>
        </v-chip>
      </v-flex>
    </v-layout>
  </v-list-tile>

</div>
</template>

<script>
// import Constants from '../lib/Constants'
import BudgetDB from '../lib/BudgetDB'
import Format from '../lib/Format'

export default {
  name: 'BudgetMonth',

  props: ['month'],

  mounted () {
    var self = this
    BudgetDB.loadCategoryDataByMonth(this.month.value - 1)
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
        console.log(err)
      })
  },

  // computed: {},

  methods: {
    budgetDetails: function () {
      alert(this.month.text)
    }
  },

  data () {
    return {
      format: Format,
      dataLoaded: false,
      monthData: {}
    }
  }
}
</script>
