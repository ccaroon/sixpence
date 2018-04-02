<template>
<div>

  <v-list-tile :class="entryColor">
    <v-list-tile-avatar>
      <v-icon>mdi-currency-usd-off</v-icon>
    </v-list-tile-avatar>
    <v-layout row align-center>
      <v-flex xs1>{{ entryType }}</v-flex>
      <v-flex xs2>{{ entry.category }}</v-flex>
      <template v-if="entry.category.startsWith('UNBUDGETED')">
        <v-flex xs2 text-xs-center>{{ format.formatMoney(entry.amount) }}</v-flex>
        <v-flex xs6><v-progress-linear value="100" height="20" color="red accent-1"></v-progress-linear></v-flex>
        <v-flex xs1 text-xs-center>N/A</v-flex>
      </template>
      <template v-else>
        <v-flex xs2 text-xs-center>{{ format.formatMoney(entry.amount) }} / {{ format.formatMoney(entry.budgetedAmount+0.0) }}</v-flex>
        <v-flex xs6><v-progress-linear v-model="progressPercent" height="20" :color="progressColor"></v-progress-linear></v-flex>
        <v-flex xs1 text-xs-center>{{ progressPercent }}%</v-flex>
      </template>
    </v-layout>
  </v-list-tile>

</div>
</template>

<script>
import Format from '../lib/Format'
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

      color = this.entry.amount === 0 ? 'grey lighten-5' : 'grey lighten-1'

      return (color)
    },

    progressPercent: function () {
      var p = (this.entry.amount / this.entry.budgetedAmount) * 100
      return Math.round(Math.abs(p))
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
      format: Format
    }
  }
}
</script>
