<template>
  <div>
    <v-list-item :class="rowColor(month)">
      <v-list-item-avatar>
        <v-icon>{{ month.icon }}</v-icon>
      </v-list-item-avatar>
      <v-layout align-center>
        <v-flex xs2>
          <span class="subtitle-1">{{ month.text }}</span>
        </v-flex>
        <v-flex xs10>
          <v-layout align-center>
            <v-flex
              xs2
              text-center
            >{{ format.formatMoney(data.amount) }} / {{ format.formatMoney(Math.abs(data.budgetedAmount+0.0)) }}</v-flex>
            <v-flex xs6>
              <v-progress-linear :value="progressPercent" height="20" :color="progressColor"></v-progress-linear>
            </v-flex>
            <v-flex xs1 text-center>{{ progressPercent }}%</v-flex>
          </v-layout>
        </v-flex>
      </v-layout>
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
