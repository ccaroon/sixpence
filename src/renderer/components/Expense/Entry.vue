<template>
  <div>
    <v-list-item :class="entryColor()">
      <v-list-item-icon>
        <v-icon>{{ entry.icon }}</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-subtitle>{{ entryType }}</v-list-item-subtitle>
        <v-list-item-title class="body-1">{{ entry.category }}</v-list-item-title>
      </v-list-item-content>

      <v-list-item-content>
        <v-list-item-subtitle>{{ format.formatDate(entry.date) }}</v-list-item-subtitle>
        <v-list-item-title class="body-1">{{ format.formatMoney(entry.amount) }}</v-list-item-title>
      </v-list-item-content>

      <v-list-item-content>
        <v-list-item-title v-if="entry.tags">
          <v-chip
            v-for="(tag, index) in entry.tags"
            :key="index"
            small
            :color="entryColor('tag')"
            @click="search(tag)"
          >{{ tag }}</v-chip>
        </v-list-item-title>
        <v-list-item-title v-else class="body-1">{{ entry.notes }}</v-list-item-title>
      </v-list-item-content>

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
        <v-card-text>
          <v-list dense :class="entryColor()">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>{{ entry.icon }}</v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-subtitle>{{ entryType }}</v-list-item-subtitle>
                <v-list-item-title class="body-1">{{ entry.category }}</v-list-item-title>
              </v-list-item-content>

              <v-list-item-content>
                <v-list-item-subtitle>{{ format.formatDate(entry.date) }}</v-list-item-subtitle>
                <v-list-item-title class="body-1">{{ format.formatMoney(entry.amount) }}</v-list-item-title>
              </v-list-item-content>

              <v-list-item-content>
                <v-list-item-title v-if="entry.tags">
                  <v-chip
                    v-for="(tag, index) in entry.tags"
                    :key="index"
                    small
                    :color="entryColor('tag')"
                  >{{ tag }}</v-chip>
                </v-list-item-title>
                <v-list-item-title v-else class="body-1">{{ entry.notes }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
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
      const type = this.entry.type === Constants.TYPE_INCOME ? 'Income' : 'Expense'
      return (type)
    }
  },

  methods: {
    entryColor: function (type = 'base') {
      let entryColor = null
      let tagColor = null

      if (this.entryNum % 2 === 0) {
        entryColor = (this.entry.amount >= 0) ? Constants.COLORS.INCOME : Constants.COLORS.EXPENSE
        tagColor = (this.entry.amount >= 0) ? Constants.COLORS.INCOME_ALT : Constants.COLORS.EXPENSE_ALT
      } else {
        entryColor = (this.entry.amount >= 0) ? Constants.COLORS.INCOME_ALT : Constants.COLORS.EXPENSE_ALT
        tagColor = (this.entry.amount >= 0) ? Constants.COLORS.INCOME : Constants.COLORS.EXPENSE
      }

      let color = entryColor
      if (type === 'tag') {
        color = tagColor
      }

      return (color)
    },

    search: function (term) {
      this.$emit('search', term)
    },

    editEntry: function () {
      this.$emit('editEntry', this.entry)
    },

    deleteEntry: function (id) {
      const self = this

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
