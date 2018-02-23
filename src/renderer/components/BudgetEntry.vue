<template>
<v-list-tile :class="entryColor">
  <v-list-tile-avatar>
    <v-icon>{{ entry.icon }}</v-icon>
  </v-list-tile-avatar>
  <v-layout row>
    <v-flex xs1>{{ entryType }}</v-flex>
    <v-flex xs3>{{ entry.category }}</v-flex>
    <v-flex xs2>{{ utils.formatMoney(entry.amount) }}</v-flex>
    <v-flex xs2>{{ utils.formatFrequency(entry.frequency) }} / {{ utils.monthNumberToName(entry.first_due - 1 )}}</v-flex>
    <v-flex xs3>{{ entry.notes }}</v-flex>
    <v-flex xs1>
      <!-- <v-btn flat icon color="black"> -->
        <v-icon>mdi-delete-forever</v-icon>
      <!-- </v-btn> -->
    </v-flex>
  </v-layout>
</v-list-tile>
</template>

<script>
import Utils from '../lib/utils'

export default {
  name: 'BudgetEntry',

  props: ['entry'],

  computed: {
    entryType: function () {
      var type = this.entry.amount >= 0 ? 'Income' : 'Expense'
      return (type)
    },
    entryColor: function () {
      var color = this.entry.amount >= 0 ? 'green accent-1' : 'red accent-1'
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
