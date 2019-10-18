<template>
  <div>
    <v-list-item :class="entryColor">
      <v-list-item-avatar>
        <v-icon>{{ entry.icon }}</v-icon>
      </v-list-item-avatar>
      <v-layout>
        <v-flex xs1>{{ entryType }}</v-flex>
        <v-flex xs3>{{ entry.category }}</v-flex>
        <v-flex xs3>{{ format.formatDate(entry.date) }}</v-flex>
        <v-flex xs2>{{ format.formatMoney(entry.amount) }}</v-flex>
        <v-flex xs>{{ entry.notes }}</v-flex>
      </v-layout>
      <v-list-item-action>
        <v-btn text icon @click="editEntry()" tabindex="-1">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
      </v-list-item-action>
      <v-list-item-action>
        <v-btn text icon @click="showDeleteDialog = true" tabindex="-1">
          <v-icon>mdi-delete-forever</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>

    <v-dialog v-model="showDeleteDialog" persistent max-width="65%">
      <v-card>
        <v-card-title class="headline">Delete Entry</v-card-title>
        <v-divider></v-divider>
        <v-card-text :class="entryColor">
          <v-layout>
            <v-flex>{{ entryType }}</v-flex>
            <v-flex>{{ format.formatDate(entry.date) }}</v-flex>
            <v-flex>{{ entry.category }}</v-flex>
            <v-flex>{{ format.formatMoney(entry.amount) }}</v-flex>
            <v-flex>{{ entry.notes }}</v-flex>
          </v-layout>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn
            color="green darken-1"
            small
            rounded
            @click="deleteEntry(entry._id)"
            tabindex="-1"
          >OK</v-btn>
          <v-btn
            color="red darken-1"
            small
            rounded
            @click.native="showDeleteDialog = false"
            tabindex="-1"
          >Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import Format from '../../lib/Format'
import Constants from '../../lib/Constants'
import ExpenseDB from '../../lib/ExpenseDB'

export default {
  name: 'ExpenseEntry',

  props: ['entryNum', 'entry'],

  computed: {
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
    editEntry: function () {
      this.$emit('editEntry', this.entry)
    },

    deleteEntry: function (id) {
      var self = this

      this.showDeleteDialog = false

      ExpenseDB.delete(id)
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
