<template>
  <div>
    <!-- Unbudgeted entries -->
    <template v-if="Array.isArray(entry)">
      <v-expansion-panels tabindex="-1" v-show="entry.length > 0">
        <v-expansion-panel tabindex="-1" :class="entryColor" expand-icon="mdi-chevron-down">
          <v-expansion-panel-header>
            <v-row dense>
              <v-col cols="4">
                <span class="title">Unbudgeted</span>
              </v-col>
              <v-col cols="2" text-left>
                <span class="title green--text">{{ format.formatMoney(unbudgetedIncome) }}</span>
              </v-col>
              <v-col cols="2" text-left>
                <span class="title red--text">{{ format.formatMoney(unbudgetedExpense) }}</span>
              </v-col>
            </v-row>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-list dense>
              <v-list-item
                @click="viewEntries(item.category)"
                :class="unbudgetedEntryColor(item)"
                v-for="(item,i) in entry"
                :key="i"
              >
                <v-list-item-icon>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                  <v-list-item-subtitle>{{ entryType(item) }}</v-list-item-subtitle>
                  <v-list-item-title class="title">{{ item.category }}</v-list-item-title>
                </v-list-item-content>

                <v-list-item-content>
                  <v-list-item-title class="title">{{ format.formatMoney(item.amount) }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </template>
    <template v-else>
      <v-list-item :class="entryColor" @click="viewEntries(entry.category)">
        <v-list-item-icon>
          <v-icon>{{ entry.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-subtitle>{{ entryType(entry) }}</v-list-item-subtitle>
          <v-list-item-title class="title">{{ entry.category }}</v-list-item-title>
        </v-list-item-content>

        <v-list-item-content>
          <v-list-item-subtitle>{{ format.formatMoney(Math.abs(entry.budgetedAmount+0.0)) }}</v-list-item-subtitle>
          <v-list-item-title class="title">{{ format.formatMoney(entry.amount) }}</v-list-item-title>
        </v-list-item-content>

        <v-list-item-content>
          <v-progress-linear
            :value="progressPercent"
            height="20"
            :color="progressColor"
          >{{ progressPercent }}%</v-progress-linear>
        </v-list-item-content>
      </v-list-item>
    </template>
  </div>
</template>

<script>
import Format from '../../lib/Format'
import Constants from '../../lib/Constants'

export default {
  name: 'ExpenseCategory',

  props: ['entryNum', 'entry'],

  computed: {
    unbudgetedIncome: function () {
      var total = 0.0
      this.entry.forEach(function (e) {
        if (e.amount >= 0.0) {
          total += e.amount
        }
      })
      return (total)
    },

    unbudgetedExpense: function () {
      var total = 0.0
      this.entry.forEach(function (e) {
        if (e.amount < 0.0) {
          total += e.amount
        }
      })
      return (total)
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

      color = total === 0 ? Constants.COLORS.GREY_ALT : Constants.COLORS.GREY

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

    unbudgetedEntryColor: function (entry) {
      var amount = Math.abs(entry.amount)

      var color
      if (entry.type === Constants.TYPE_INCOME) {
        color = Constants.COLORS.INCOME
      } else {
        if (amount <= 100) {
          color = 'red lighten-5'
        } else if (amount > 100 && amount <= 200) {
          color = 'red lighten-3'
        } else if (amount > 200) {
          color = Constants.COLORS.EXPENSE_ALT
        }
      }

      return (color)
    },

    entryType: function (entry) {
      var type = entry.type === Constants.TYPE_INCOME ? 'Income' : 'Expense'
      return (type)
    },

    viewEntries: function (category) {
      this.$emit('viewEntriesInGroup', category, this.entryTotal)
    }
  },

  data () {
    return {
      format: Format
    }
  }
}
</script>

<style scoped>
.lowerCaseButton {
  text-transform: none !important;
  text-align: left !important;
}
</style>
