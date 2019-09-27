<template>
  <div>
    <v-list-tile :class="entryColor">
      <v-list-tile-avatar>
        <v-icon>{{ entry.icon }}</v-icon>
      </v-list-tile-avatar>
      <v-layout row>
        <v-flex xs1>{{ entryType }}</v-flex>
        <v-flex xs3>{{ entry.category }}</v-flex>
        <v-flex xs2>{{ format.formatMoney(entry.amount) }}</v-flex>
        <v-flex
          xs2
        >{{ format.formatFrequency(entry.frequency) }} / {{ format.monthNumberToName(entry.firstDue - 1 )}}</v-flex>
        <v-flex xs>{{ entry.notes }}</v-flex>
      </v-layout>
      <template v-if="!readOnly">
        <v-list-tile-action>
          <v-btn flat icon :disabled="!entry.history" @click="viewHistory()" tabindex="-1">
            <v-icon>mdi-history</v-icon>
          </v-btn>
        </v-list-tile-action>
        <v-list-tile-action>
          <v-btn flat icon @click="editEntry()" tabindex="-1">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-list-tile-action>
        <v-list-tile-action>
          <v-btn flat icon @click="showRemoveDialog = true" tabindex="-1">
            <v-icon>mdi-delete-forever</v-icon>
          </v-btn>
        </v-list-tile-action>
      </template>
      <template v-else>Archived: {{ format.formatDate(entry.archivedAt) }}</template>
    </v-list-tile>

    <!--  HISTORY -->
    <template v-if="entry.history">
      <v-dialog v-model="showHistory" max-width="768">
        <v-card>
          <v-card-title :id="entry._id" :class="entryColor" class="headline">
            <v-icon color="black">{{ entry.icon }}</v-icon>
            {{ entry.category }} - Record History
          </v-card-title>
          <v-card-text>
            <v-icon color="info">mdi-alert-circle</v-icon>Currently only tracking changes to budgeted amounts.
            <v-list>
              <v-list-tile
                v-for="(record, index) in entry.history"
                :key="record.date"
                :class="altColors(index)"
              >
                <v-layout row>
                  <v-flex xs1>
                    <v-list-tile-content>
                      <v-icon>mdi-calendar</v-icon>
                    </v-list-tile-content>
                  </v-flex>
                  <v-flex xs4>
                    <v-list-tile-content>{{ format.formatDate(record.date, 'MMM DD, YYYY @ hh:mm:ss') }}</v-list-tile-content>
                  </v-flex>
                  <v-flex xs7>
                    <v-list-tile-content v-if="index < entry.history.length-1">
                      {{ format.formatMoney(record.amount) }}
                      &rarr;
                      {{ format.formatMoney(entry.history[index+1].amount) }}
                    </v-list-tile-content>
                    <v-list-tile-content v-else>
                      {{ format.formatMoney(record.amount) }}
                      &rarr;
                      {{ format.formatMoney(entry.amount) }}
                    </v-list-tile-content>
                  </v-flex>
                </v-layout>
              </v-list-tile>
            </v-list>
          </v-card-text>
        </v-card>
      </v-dialog>
    </template>

    <v-dialog v-model="showRemoveDialog" persistent max-width="65%">
      <v-card>
        <v-card-title class="headline">Remove Entry</v-card-title>
        <v-divider></v-divider>
        <v-card-text :class="entryColor">
          <v-layout row>
            <v-flex>{{ entryType }}</v-flex>
            <v-flex>{{ entry.category }}</v-flex>
            <v-flex>{{ format.formatMoney(entry.amount) }}</v-flex>
            <v-flex>{{ format.formatFrequency(entry.frequency) }} / {{ format.monthNumberToName(entry.firstDue - 1 )}}</v-flex>
            <v-flex>{{ entry.notes }}</v-flex>
          </v-layout>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="green darken-1" small round @click="archiveEntry(entry)" tabindex="-1">
            <v-icon left>mdi-package-down</v-icon>Archive
          </v-btn>
          <v-btn color="red darken-2" small round @click="deleteEntry(entry._id)" tabindex="-1">
            <v-icon left>mdi-delete-forever</v-icon>Delete Forever
          </v-btn>
          <v-btn
            color="red lighten-1"
            small
            round
            right
            absolute
            @click.native="showRemoveDialog = false"
            tabindex="-1"
          >
            <v-icon left>mdi-cancel</v-icon>Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Constants from '../../lib/Constants'
import BudgetDB from '../../lib/BudgetDB'
import Format from '../../lib/Format'

export default {
  name: 'BudgetEntry',
  props: ['entryNum', 'entry', 'readOnly'],

  computed: {
    hasHistory: function () {
      var hasHistory = this.entry.history ? '' : 'disabled'
      return hasHistory
    },

    entryType: function () {
      var type = this.entry.type === Constants.TYPE_INCOME ? 'Income' : 'Expense'
      return (type)
    },

    entryColor: function () {
      var color = null

      if (this.entryNum % 2 === 0) {
        color = (this.entry.amount >= 0) ? Constants.COLORS.INCOME : Constants.COLORS.EXPENSE
      } else {
        color = (this.entry.amount >= 0) ? Constants.COLORS.INCOME_ALT : Constants.COLORS.EXPENSE_ALT
      }

      return (color)
    }
  },

  methods: {
    altColors: function (value) {
      var color = Constants.COLORS.GREY
      if (value % 2 === 0) {
        color = Constants.COLORS.GREY_ALT
      }

      return (color)
    },

    archiveEntry: function (entry) {
      var self = this

      this.showRemoveDialog = false

      entry.archivedAt = new Date()
      BudgetDB.save(entry)
        .then((num, upsert) => {
          self.$emit('refreshData')
          self.$emit('displayAlert', 'mdi-package-down', 'green', 'Archive Successful!')
        })
        .catch(err => {
          self.$emit('displayAlert', 'mdi-package-down', 'red', err)
        })
    },

    editEntry: function () {
      this.$emit('editEntry', this.entry)
    },

    viewHistory: function () {
      this.showHistory = true
    },

    deleteEntry: function (id) {
      var self = this

      this.showRemoveDialog = false

      BudgetDB.delete(id)
        .then(function (numDeleted) {
          self.$emit('refreshData')
          self.$emit('displayAlert', 'mdi-delete', 'green', 'Delete Successful!')
        })
        .catch(function (err) {
          self.$emit('displayAlert', 'mdi-delete', 'red', err)
        })
    }
  },

  data () {
    return {
      format: Format,
      showRemoveDialog: false,
      showHistory: false
    }
  }
}
</script>
