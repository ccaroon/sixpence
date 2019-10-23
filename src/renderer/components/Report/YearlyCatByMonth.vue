<template>
  <div>
    <v-list-item :class="rowColor(month)">
      <v-list-item-icon>
        <v-icon>{{ month.icon }}</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title class="body-1">{{ month.text }}</v-list-item-title>
      </v-list-item-content>

      <v-list-item-content>
        <v-list-item-subtitle>{{ format.formatMoney(Math.abs(data.budgetedAmount+0.0)) }}</v-list-item-subtitle>
        <v-list-item-title class="body-1">{{ format.formatMoney(data.amount) }}</v-list-item-title>
      </v-list-item-content>

      <v-list-item-content>
        <v-progress-linear
          :value="progressPercent"
          height="20"
          :color="progressColor"
        >{{ progressPercent }}%</v-progress-linear>
      </v-list-item-content>
    </v-list-item>
  </div>
</template>

<script>
import Constants from '../../lib/Constants'
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
        color = Constants.COLORS.PROGRESS_GOOD
      } else if (p > 75 && p < 100) {
        color = Constants.COLORS.PROGRESS_WARN
      } else if (p === 100) {
        color = Constants.COLORS.PROGRESS_BULLSEYE
      } else {
        color = Constants.COLORS.PROGRESS_DANGER
      }

      return color
    }
  },

  methods: {
    rowColor: function (month) {
      var color = month.value % 2 === 0 ? Constants.COLORS.GREY : Constants.COLORS.GREY_ALT
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
