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
      <v-flex xs2>{{ format.formatFrequency(entry.frequency) }} / {{ format.monthNumberToName(entry.firstDue - 1 )}}</v-flex>
      <v-flex xs>{{ entry.notes }}</v-flex>
    </v-layout>
    <v-list-tile-action>
      <v-btn flat icon @click="editEntry()" tabindex="-1">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
    </v-list-tile-action>
    <v-list-tile-action>
      <v-btn flat icon @click="showDeleteDialog = true" tabindex="-1">
        <v-icon>mdi-delete-forever</v-icon>
      </v-btn>
    </v-list-tile-action>
  </v-list-tile>

  <v-dialog v-model="showDeleteDialog" persistent max-width="65%">
    <v-card>
      <v-card-title class="headline">Delete Entry</v-card-title>
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
        <v-btn color="green darken-1"
          small round @click="deleteEntry(entry._id)" tabindex="-1">
          OK
        </v-btn>
        <v-btn color="red darken-1"
          small round @click.native="showDeleteDialog = false" tabindex="-1">
          Cancel
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

  props: ['entry'],

  computed: {
    entryType: function () {
      var type = this.entry.type === Constants.TYPE_INCOME ? 'Income' : 'Expense'
      return (type)
    },
    entryColor: function () {
      var color = this.entry.amount >= 0 ? 'green accent-1' : 'red accent-1'
      return (color)
    }
  },

  methods: {
    editEntry: function () {
      this.$emit('editEntry', this.entry)
    },

    deleteEntry: function (id) {
      var self = this

      this.showDeleteDialog = false

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
      showDeleteDialog: false
    }
  }
}
</script>
