<template>
<div>

  <v-list-tile :class="entryColor">
    <v-list-tile-avatar>
      <v-icon>mdi-currency-usd-off</v-icon>
    </v-list-tile-avatar>
    <v-layout row>
      <v-flex xs1>{{ entryType }}</v-flex>
      <v-flex xs2>{{ entry.category }}</v-flex>
      <v-flex xs2>{{ utils.formatMoney(entry.amount) }} / {{ utils.formatMoney(entry.budgetedAmount+0.0) }}</v-flex>
      <v-flex xs1>{{ progressPercent }}%</v-flex>
      <v-flex>
        <v-progress-linear v-model="progressPercent" height="10" :color="progressColor"></v-progress-linear>
      </v-flex>
    </v-layout>
  </v-list-tile>

</div>
</template>

<script>
import Utils from '../lib/utils'
import Constants from '../lib/Constants'

export default {
  name: 'ExpenseCategory',

  props: ['entry'],

  computed: {
    entryType: function () {
      var type = this.entry.type === Constants.TYPE_INCOME ? 'Income' : 'Expense'
      return (type)
    },
    entryColor: function () {
      var color
      if (this.entry.amount === 0) {
        color = 'grey lighten-5'
      } else if (this.entry.amount > 0) {
        color = 'green lighten-5'
      } else {
        color = 'red lighten-5'
      }
      return (color)
    },
    progressPercent: function () {
      var p = (this.entry.amount / this.entry.budgetedAmount) * 100
      return Math.round(p)
    },
    progressColor: function () {
      var p = this.progressPercent
      var color
      if (p === 0) {
        color = 'white'
      } else if (p <= 75) {
        color = 'green accent-1'
      } else if (p > 75 && p <= 100) {
        color = 'yellow accent-1'
      } else {
        color = 'red accent-1'
      }

      return color
    }
  },

  methods: {
  },

  data () {
    return {
      utils: Utils
    }
  }
}
</script>
