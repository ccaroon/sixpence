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
          @click:event="true"
          @click:date="true"
        >
        </v-calendar>
      </v-sheet>
    </div>
  </v-container>
</template>
<script>
import Moment from 'moment'

import Format from '../../lib/Format'

export default {
  name: 'expenses-calendar',
  components: { },
  mounted: function () {},

  methods: {
    // goToToday: function () {
    //   this.calDate = Format.formatDate(new Date(), 'YYYY-MM-DD')
    // },

    eventColor: function (day) {
      const color = 'blue'
      return color
    },

    createEvents: function (days) {
      const events = []

      // TODO: Each Event
      // Income
      // Expense
      // Balance
      days.forEach((day) => {
        let name = day.typeCode()
        if (day.note) {
          name += ` - ${day.note}`
        }
        events.push({
          name: name,
          start: day.start().toDate(),
          end: day.end().toDate(),
          color: this.eventColor(day),
          timed: !day.allDay(),
          workDay: day
        })
      })

      return events
    },

    refresh: function () {
      this.loadMonth()
    },

    loadMonth: function () {
      const self = this
      self.events = {}
    //   self.createEvents(days)
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
      calDate: Format.formatDate(new Date(), 'YYYY-MM-DD'),
      events: [],
      // selectedCalEvent: {},
      // eventElement: null,
      format: Format
    }
  }
}
</script>
