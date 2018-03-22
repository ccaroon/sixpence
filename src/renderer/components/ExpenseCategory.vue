<template>
<div>

  <v-list-tile :class="entryColor">
    <v-list-tile-avatar>
      <v-icon>mdi-currency-usd-off</v-icon>
    </v-list-tile-avatar>
    <v-layout row>
      <v-flex xs1>{{ entryType }}</v-flex>
      <v-flex xs3>{{ entry.category }}</v-flex>
      <v-flex xs2>{{ utils.formatMoney(entry.amount) }}</v-flex>
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
        color = 'grey lighten-2'
      } else if (this.entry.amount > 0) {
        color = 'green accent-1'
      } else {
        color = 'red accent-1'
      }
      return (color)
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
