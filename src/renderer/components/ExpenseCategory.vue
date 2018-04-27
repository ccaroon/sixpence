<template>
<div>

  <!-- ASSUME it's the UNBUDGETED entries -->
  <template v-if="Array.isArray(entry)">
    <v-expansion-panel>
      <v-expansion-panel-content :class="entryColor" expand-icon="mdi-chevron-down">
        <v-layout row slot="header">
          <v-flex xs4 class="title">Unbudgeted Expenses</v-flex>
          <v-flex xs2 class="title" text-xs-left>{{ format.formatMoney(entryTotal) }}</v-flex>
        </v-layout>
        <v-list>
          <v-list-tile class="grey lighten-1" v-for="(item,i) in entry" :key="i">
            <v-list-tile-avatar>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-avatar>
            <v-layout row align-center>
              <v-flex xs1>{{ entryType }}</v-flex>
              <v-flex xs2>{{ item.category }}</v-flex>
              <v-flex xs2 text-xs-center>{{ format.formatMoney(item.amount) }}</v-flex>
            </v-layout>
          </v-list-tile>
        </v-list>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </template>
  <template v-else>
    <v-list-tile :class="entryColor">
      <v-list-tile-avatar>
        <v-icon>{{ entry.icon }}</v-icon>
      </v-list-tile-avatar>
      <v-layout row align-center>
        <v-flex xs1>{{ entryType }}</v-flex>
        <v-flex xs2>{{ entry.category }}</v-flex>
        <v-flex xs2 text-xs-center>{{ format.formatMoney(entry.amount) }} / {{ format.formatMoney(Math.abs(entry.budgetedAmount+0.0)) }}</v-flex>
        <v-flex xs6><v-progress-linear v-model="progressPercent" height="20" :color="progressColor"></v-progress-linear></v-flex>
        <v-flex xs1 text-xs-center>{{ progressPercent }}%</v-flex>
      </v-layout>
    </v-list-tile>
  </template>

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

    entryTotal: function () {
      var total = 0.0
      if (Array.isArray(this.entry)) {
        this.entry.forEach(function (e) {
          total += e.amount
        })
      } else {
        total = this.entry.amount
      }

      return (total)
    },

    entryColor: function () {
      var color
      var total = this.entryTotal

      color = total === 0 ? 'grey lighten-5' : 'grey lighten-1'

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
      } else if (p > 75 && p < 100) {
        color = 'yellow accent-1'
      } else if (p === 100) {
        color = 'green accent-3'
      } else {
        color = 'red accent-2'
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
