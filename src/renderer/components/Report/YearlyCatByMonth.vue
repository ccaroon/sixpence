<template>
<div>
  <v-list-tile :class="rowColor(month)">
    <v-list-tile-avatar>
      <v-icon>{{ month.icon }}</v-icon>
    </v-list-tile-avatar>
    <v-layout row align-center>
      <v-flex xs2><span class="subheading">{{ month.text }}</span></v-flex>
      <v-flex xs10>
        <v-layout row align-center>
          <v-flex xs2 text-xs-center>{{ format.formatMoney(data.amount) }} / {{ format.formatMoney(Math.abs(data.budgetedAmount+0.0)) }}</v-flex>
          <v-flex xs6><v-progress-linear v-model="progressPercent" height="20" :color="progressColor"></v-progress-linear></v-flex>
          <v-flex xs1 text-xs-center>{{ progressPercent }}%</v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-list-tile>
</div>
</template>

<script>
import Format from '../../lib/Format'

export default {
  name: 'YearlyCatByMonth',

  props: ['month', 'data'],

  mounted () {},

  computed: {
    progressPercent: function () {
      var percent = 0.0
      if (this.data.budgetedAmount !== 0.0) {
        percent = (this.data.amount / this.data.budgetedAmount) * 100
      }

      return Math.round(Math.abs(percent))
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
    rowColor: function (month) {
      var color = month.value % 2 === 0 ? 'grey lighten-4' : 'grey lighten-2'
      return (color)
    }
  },

  data () {
    return {
      format: Format
    }
  }
}
</script>
