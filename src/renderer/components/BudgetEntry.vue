<template>
<v-list-tile :class="entryColor">
  <v-list-tile-avatar>
    <v-icon>mdi-{{ entry.icon }}</v-icon>
  </v-list-tile-avatar>
  <v-layout row>
    <v-flex xs1>{{ entryType }}</v-flex>
    <v-flex xs4>{{ entry.category }}</v-flex>
    <v-flex xs2>{{ formattedAmount }}</v-flex>
    <v-flex xs2> {{ frequency }} / {{ monthToName(entry.first_due - 1 )}}</v-flex>
    <v-flex>{{ entry.notes }}</v-flex>
  </v-layout>
  <!--
  <v-list-tile-avatar>
    <v-icon>mdi-currency-usd</v-icon>
  </v-list-tile-avatar>
  <v-list-tile-content>
    <v-list-tile-title>Title</v-list-tile-title>
    <v-list-tile-sub-title>{{ dbPath }}</v-list-tile-sub-title>
  </v-list-tile-content> -->
  <!-- <v-text-field box label="First Name" v-model="first"></v-text-field> -->
</v-list-tile>
</template>

<script>
export default {
  name: 'BudgetEntry',

  props: ['entry'],

  computed: {
    frequency: function () {
      var freqStr = null

      switch (this.entry.frequency) {
        case 1:
          freqStr = 'Monthly'
          break
        case 2:
          freqStr = 'Bi-Montly'
          break
        case 3:
          freqStr = 'Quarterly'
          break
        case 6:
          freqStr = 'Bi-Yearly'
          break
        case 12:
          freqStr = 'Yearly'
          break
        default:
          freqStr = 'Every ' + this.entry.frequency + ' Months'
          break
      }

      return (freqStr)
    },

    formattedAmount: function () {
      var amt = this.entry.amount.toLocaleString('en-US', {style: 'currency', currency: 'USD'})

      return (amt)
    },
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
    monthToName: function (monthNumber) {
      var d = new Date()
      d.setMonth(monthNumber)
      return (d.toLocaleDateString('en-US', {month: 'long'}))
    }
  },

  data () {
    return {}
  }
}
</script>
