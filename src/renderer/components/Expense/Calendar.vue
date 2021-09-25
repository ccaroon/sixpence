<template>
  <v-container>
    <div>
      <v-sheet tile class="d-flex">
        <v-spacer></v-spacer>
        <span class="text-h4">{{
          format.formatDate(calDate, "MMMM YYYY")
        }}</span>
        <v-spacer></v-spacer>
      </v-sheet>
      <v-sheet height="825">
        <v-calendar
          ref="calendar"
          v-model="calDate"
          color="orange"
          event-text-color="black"
          :event-more="false"
          :events="events"
          @click:event="viewEntries"
          @click:date="addEntry"
        >
        </v-calendar>
      </v-sheet>
    </div>
  </v-container>
</template>
<script>
import Moment from 'moment'

import Constants from '../../lib/Constants'
import Format from '../../lib/Format'

export default {
  name: 'expenses-calendar',
  props: ['expenses', 'monthToView', 'newEntry'],
  components: { },
  mounted: function () {
    this.refresh()
  },

  methods: {
    createEvents: function () {
      const events = []

      const entriesByDate = new Map()
      this.expenses.forEach((entry) => {
        const entryDate = Moment(entry.date).startOf('day')
        const entryKey = entryDate.unix()

        let dayEntry = entriesByDate.get(entryKey)
        if (dayEntry === undefined) {
          dayEntry = {
            date: entryDate,
            income: 0.0,
            expenses: 0.0
          }
          entriesByDate.set(entryKey, dayEntry)
        }

        if (entry.amount < 0.0) {
          dayEntry.expenses += entry.amount
        } else if (entry.amount >= 0.0) {
          dayEntry.income += entry.amount
        }
      })

      entriesByDate.forEach((entry) => {
        if (entry.income > 0.0) {
          events.push({
            name: Format.formatMoney(entry.income),
            start: entry.date.toDate(),
            end: entry.date.toDate(),
            color: Constants.COLORS.INCOME,
            timed: false,
            entryType: Constants.TYPE_INCOME
          })
        }

        if (entry.expenses < 0.0) {
          events.push({
            name: Format.formatMoney(entry.expenses),
            start: entry.date.toDate(),
            end: entry.date.toDate(),
            color: Constants.COLORS.EXPENSE,
            timed: false,
            entryType: Constants.TYPE_EXPENSE
          })
        }
      })

      return events
    },

    addEntry: function (dateEvent) {
      const entryDate = Moment(dateEvent.date)
      this.newEntry(entryDate)
    },

    viewEntries: function (event) {
      this.$emit('viewEntriesInGroup', `date?${event.day.date}&type?${event.event.entryType}`)
    },

    refresh: function () {
      this.loadMonth()
    },

    loadMonth: function () {
      const self = this
      self.events = self.createEvents()
    }
  },

  watch: {
    calDate: function (newDate, oldDate) {
      if (!Moment(oldDate).isSame(newDate, 'month')) {
        this.refresh()
      }
    }
  },

  data () {
    return {
      calDate: Format.formatDate(this.monthToView, 'YYYY-MM-DD'),
      events: [],
      format: Format
    }
  }
}
</script>
