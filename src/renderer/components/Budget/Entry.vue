<template>
  <div>
    <v-list-item :class="entryColor">
      <v-list-item-icon>
        <v-icon>{{ entry.icon }}</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-subtitle>{{ entryType }}</v-list-item-subtitle>
        <v-list-item-title class="body-1">{{ entry.category }}</v-list-item-title>
      </v-list-item-content>

      <v-list-item-content>
        <v-list-item-subtitle>{{ format.formatFrequency(entry.frequency) }} / {{ format.monthNumberToName(entry.firstDue - 1 )}}</v-list-item-subtitle>
        <v-list-item-title class="body-1">{{ format.formatMoney(entry.amount) }}</v-list-item-title>
      </v-list-item-content>

      <v-list-item-content>
        <v-list-item-title class="body-1">{{ entry.notes }}</v-list-item-title>
      </v-list-item-content>

      <template v-if="!readOnly">
        <v-list-item-action>
          <v-btn icon :disabled="!entry.history" @click="viewHistory()" tabindex="-1">
            <v-icon>mdi-history</v-icon>
          </v-btn>
        </v-list-item-action>

        <v-list-item-action>
          <v-btn icon @click="editEntry()" tabindex="-1">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-list-item-action>

        <v-list-item-action>
          <v-btn icon @click="showRemoveDialog = true" tabindex="-1">
            <v-icon>mdi-delete-forever</v-icon>
          </v-btn>
        </v-list-item-action>
      </template>
      <template v-else>
        <v-list-item-content>
          <v-list-item-title>Archived: {{ format.formatDate(entry.archivedAt) }}</v-list-item-title>
        </v-list-item-content>
      </template>
    </v-list-item>

    <!--  HISTORY -->
    <template v-if="entry.history">
      <v-dialog v-model="showHistory" scrollable max-width="768">
        <v-card>
          <v-card-title :id="entry._id" :class="entryColor" class="headline">
            <v-icon color="black">{{ entry.icon }}</v-icon>
            &nbsp;
            {{ entry.category }} - Record History
          </v-card-title>
          <v-card-text style="height: 75%">
            <v-icon color="info">mdi-alert-circle</v-icon>Currently only tracking changes to budgeted amounts.
            <v-list>
              <v-list-item
                v-for="(record, index) in entry.history"
                :key="record.date"
                :class="altColors(index)"
              >
                <v-list-item-icon>
                  <v-icon>mdi-calendar</v-icon>
                </v-list-item-icon>
                <v-row no-gutters>
                  <v-col cols="2">
                    <v-list-item-content>
                      <v-list-item-title>{{ format.formatDate(record.date, 'MMM DD, YYYY') }}</v-list-item-title>
                      <v-list-item-subtitle>{{ format.formatDate(record.date, 'hh:mm:ssa') }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-col>
                  <v-col cols="4">
                    <v-list-item-content>
                      <v-list-item-title v-if="index < entry.history.length-1">
                        {{ format.formatMoney(record.amount) }}
                        &rarr;
                        {{ format.formatMoney(entry.history[index+1].amount) }}
                      </v-list-item-title>
                      <v-list-item-title v-else>
                        {{ format.formatMoney(record.amount) }}
                        &rarr;
                        {{ format.formatMoney(entry.amount) }}
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-col>
                  <v-col cols="4">
                    <v-list-item-content>
                      <v-list-item-title>{{ record.note }}</v-list-item-title>
                    </v-list-item-content>
                  </v-col>
                </v-row>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-dialog>
    </template>

    <v-dialog v-model="showRemoveDialog" persistent max-width="65%">
      <v-card>
        <v-card-title class="title">Remove Entry</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-list dense :class="entryColor">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>{{ entry.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-subtitle>{{ entryType }}</v-list-item-subtitle>
                <v-list-item-title class="body-1">{{ entry.category }}</v-list-item-title>
              </v-list-item-content>

              <v-list-item-content>
                <v-list-item-subtitle>{{ format.formatFrequency(entry.frequency) }} / {{ format.monthNumberToName(entry.firstDue - 1 )}}</v-list-item-subtitle>
                <v-list-item-title class="body-1">{{ format.formatMoney(entry.amount) }}</v-list-item-title>
              </v-list-item-content>

              <v-list-item-content>
                <v-list-item-title class="body-1">{{ entry.notes }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="green darken-1" small rounded @click="archiveEntry(entry)" tabindex="-1">
            <v-icon float-left>mdi-package-down</v-icon>Archive
          </v-btn>
          <v-btn color="red darken-2" small rounded @click="deleteEntry(entry._id)" tabindex="-1">
            <v-icon float-left>mdi-delete-forever</v-icon>Delete Forever
          </v-btn>
          <v-btn
            color="red lighten-1"
            small
            rounded
            right
            absolute
            @click.native="showRemoveDialog = false"
            tabindex="-1"
          >
            <v-icon float-left>mdi-cancel</v-icon>Cancel
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
