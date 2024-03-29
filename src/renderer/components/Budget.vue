<template>
  <div>
    <v-app-bar :color="constants.COLORS.TOOLBAR" app dark fixed>
      <v-menu bottom offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item
            v-for="(item, i) in menu"
            :key="i"
            @click="setView(item)"
          >
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-row no-gutters align="center">
        <v-col cols="1">
          <v-toolbar-title id="budget-toolbar-title">Budget</v-toolbar-title>
        </v-col>
        <v-col cols="3">
          <v-toolbar-items>
            <v-btn-toggle
              id="budget-freq-filter"
              v-model="freqFilter"
              mandatory
              rounded
              dark
              :class="constants.COLORS.TOOLBAR_BUTTON"
            >
              <v-btn text>
                <v-icon>mdi-numeric-1-box</v-icon>
              </v-btn>
              <v-btn text>
                <v-icon>mdi-numeric-2-box</v-icon>
              </v-btn>
              <v-btn text>
                <v-icon>mdi-numeric-3-box</v-icon>
              </v-btn>
              <v-btn text>
                <v-icon>mdi-numeric-6-box</v-icon>
              </v-btn>
              <v-btn text>
                <v-icon>fa-calendar</v-icon>
              </v-btn>
              <v-btn text>
                <v-icon>mdi-all-inclusive</v-icon>
              </v-btn>
            </v-btn-toggle>
          </v-toolbar-items>
        </v-col>
        <v-col cols="4">
          <v-toolbar-items>
            <v-chip :color="constants.COLORS.INCOME" text-color="black">
              <v-icon float-left>{{ icons.get("Income").value }}</v-icon>
              <span class="subtitle-1">{{
                format.formatMoney(totalIncome)
              }}</span> </v-chip
            >&nbsp;
            <v-chip :color="constants.COLORS.EXPENSE" text-color="black">
              <v-icon float-left>{{ icons.get("Expense").value }}</v-icon>
              <span class="subtitle-1">{{
                format.formatMoney(totalExpenses)
              }}</span> </v-chip
            >&nbsp;
            <v-chip
              :color="
                totalIncome + totalExpenses >= 0
                  ? constants.COLORS.INCOME_ALT
                  : constants.COLORS.EXPENSE_ALT
              "
              text-color="black"
            >
              <v-icon float-left>{{ icons.get("Balance").value }}</v-icon>
              <span class="subtitle-1">{{
                format.formatMoney(totalIncome + totalExpenses)
              }}</span>
            </v-chip>
          </v-toolbar-items>
        </v-col>
        <v-col>
          <v-toolbar-items>
            <v-btn
              @click="search()"
              icon
              small
              :color="constants.COLORS.TOOLBAR_BUTTON"
            >
              <v-icon>mdi-magnify</v-icon> </v-btn
            >&nbsp;
            <v-text-field
              ref="searchField"
              v-model="searchText"
              hide-details
              color="black"
              single-line
              @keyup.enter="search()"
              @keyup.esc="clearSearch()"
            ></v-text-field>
            <v-btn
              @click="clearSearch()"
              icon
              small
              :color="constants.COLORS.TOOLBAR_BUTTON"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-toolbar-items>
        </v-col>
      </v-row>
    </v-app-bar>

    <v-snackbar
      bottom
      v-model="alert.visible"
      :color="alert.color"
      :timeout="alert.timeout"
    >
      <v-icon>{{ alert.icon }}</v-icon>
      &nbsp;{{ alert.message }}
      <v-btn icon dark @click="alert.visible = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-snackbar>

    <template
      v-if="
        view === constants.BUDGET_VIEW_SUMMARY ||
        view === constants.BUDGET_VIEW_ARCHIVED
      "
    >
      <v-list dense>
        <BudgetEntry
          v-for="(entry, index) in budget"
          :key="index"
          v-bind:entryNum="index"
          v-bind:entry="entry"
          v-bind:readOnly="
            view === constants.BUDGET_VIEW_ARCHIVED ? true : false
          "
          v-on:editEntry="editEntry"
          v-on:refreshData="refreshData"
          v-on:displayAlert="displayAlert"
        ></BudgetEntry>
      </v-list>
    </template>

    <template v-if="view === constants.BUDGET_VIEW_BYMONTH">
      <v-list dense>
        <BudgetMonth
          v-for="month in constants.MONTHS"
          :key="month.value"
          v-bind:month="month"
          v-bind:average="totalIncome + totalExpenses"
          v-on:displayAlert="displayAlert"
        ></BudgetMonth>
      </v-list>
    </template>

    <v-dialog v-model="showHistoryNoteDialog" persistent max-width="50%">
      <v-card>
        <v-card-title :class="constants.COLORS.GREY">
          <v-icon color="black">{{ entry.icon }}</v-icon>
          &nbsp;
          {{ entry.category }} - Change Note
        </v-card-title>
        <v-card-text>
          <v-text-field autofocus v-model="historyNote"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn
            small
            rounded
            @click="
              showHistoryNoteDialog = false;
              historyCallback ? historyCallback(historyNote) : false;
            "
            :color="constants.COLORS.OK_BUTTON"
            >Continue</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <div class="text-center">
      <v-bottom-sheet v-model="showAddEditSheet">
        <template v-slot:activator="{ on }">
          <v-btn
            :color="constants.COLORS.OK_BUTTON"
            @click="entry = {}"
            fixed
            bottom
            right
            dark
            fab
            small
            v-on="on"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>

        <v-card>
          <v-form ref="budgetForm">
            <v-row>
              <v-col cols="1">
                <v-autocomplete
                  ref="iconSelect"
                  :items="icons.ICONS"
                  v-model="entry.icon"
                  label="Icon"
                  single-line
                  dense
                  hint="Choose an Icon"
                  append-icon="mdi-menu-down"
                >
                  <template v-slot:selection="data">
                    <v-icon>{{ data.item.value }}</v-icon>
                  </template>
                  <template v-slot:item="data">
                    <v-icon>{{ data.item.value }}</v-icon>
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col cols="2">
                <v-combobox
                  :items="categories"
                  v-model="entry.category"
                  label="Category"
                  single-line
                  dense
                  required
                  :rules="rules.category"
                  hint="Choose a Category or Add a New One"
                  append-icon="mdi-menu-down"
                ></v-combobox>
              </v-col>
              <v-col cols="1">
                <v-text-field
                  name="amount"
                  label="Amount"
                  id="amount"
                  single-line
                  dense
                  required
                  hint="Positive for Income, Negative for Expense"
                  :rules="rules.amount"
                  v-model="entry.amount"
                ></v-text-field>
              </v-col>
              <v-col cols="2">
                <v-autocomplete
                  :items="constants.FREQUENCY"
                  v-model="entry.frequency"
                  label="Frequency"
                  single-line
                  dense
                  required
                  :rules="rules.frequency"
                  hint="How Frequently Does This Item Occur?"
                  append-icon="mdi-menu-down"
                ></v-autocomplete>
              </v-col>
              <v-col cols="2">
                <v-autocomplete
                  :items="constants.MONTHS"
                  v-model="entry.firstDue"
                  label="First Due"
                  single-line
                  dense
                  required
                  :rules="rules.firstDue"
                  hint="In What Month Is This Item First Due?"
                  append-icon="mdi-menu-down"
                ></v-autocomplete>
              </v-col>
              <v-col cols="3">
                <v-text-field
                  name="notes"
                  label="Notes"
                  id="notes"
                  v-model="entry.notes"
                  single-line
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols="1" text-center>
                <v-btn
                  :color="constants.COLORS.OK_BUTTON"
                  fab
                  small
                  @click="saveEntry()"
                >
                  <v-icon>mdi-content-save</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card>
      </v-bottom-sheet>
    </div>
  </div>
</template>

<script>
import BudgetEntry from './Budget/Entry'
import BudgetMonth from './Budget/Month'
import BudgetDB from '../lib/BudgetDB'
import Constants from '../lib/Constants'
import Format from '../lib/Format'
import Icons from '../lib/Icons'
import Mousetrap from 'mousetrap'

// const {app} = require('electron').remote
const HISTORY_FIELDS = ['amount']

export default {
  name: 'Budget',
  components: { BudgetEntry, BudgetMonth },

  mounted () {
    this._bindShortcutKeys()
    this._loadBudgetData()
  },

  computed: {
    totalIncome: function () {
      let income = 0.0
      for (let i = 0; i < this.budget.length; i++) {
        const entry = this.budget[i]
        if (entry.amount >= 0.0) {
          income += entry.amount
        }
      }
      return (income)
    },

    totalExpenses: function () {
      let expense = 0.0
      for (let i = 0; i < this.budget.length; i++) {
        const entry = this.budget[i]
        if (entry.amount < 0.0) {
          expense += (entry.amount / entry.frequency)
        }
      }
      return (expense)
    }
  },

  methods: {
    _bindShortcutKeys: function () {
      Mousetrap.bind(['ctrl+n', 'command+n'], () => {
        this.newEntry()
        return false
      })

      Mousetrap.bind(['ctrl+f', 'command+f'], () => {
        this.$refs.searchField.focus()
        return false
      })

      Mousetrap.bind('esc', () => {
        this.showAddEditSheet = false
        return false
      })
    },

    refreshData: function () {
      // search() will display active search results if any
      // otherwise it will display all entries
      this.search()
    },

    loadAllData: function () {
      this._loadBudgetData()
    },

    search: function () {
      const self = this
      const terms = []

      let freq = null
      switch (this.freqFilter) {
        case 0:
          freq = 1
          break
        case 1:
          freq = 2
          break
        case 2:
          freq = 3
          break
        case 3:
          freq = 6
          break
        case 4:
          freq = 12
          break
        case 5:
          freq = null
          break
        default:
          freq = null
          break
      }

      if (freq) {
        terms.push({ frequency: freq })
      }

      if (this.searchText) {
        const parts = this.searchText.split(/\?/, 2)

        if (parts.length === 2) {
          const fieldQuery = {}
          fieldQuery[parts[0].trim()] = new RegExp(parts[1].trim(), 'i')

          terms.push(fieldQuery)
        } else {
          terms.push({ category: new RegExp(parts[0].trim(), 'i') })
        }
      }

      if (terms.length !== 0) {
        terms.push({ archivedAt: null })
        const query = { $and: terms }

        BudgetDB.search(query)
          .then(function (docs) {
            self.budget = docs
          })
          .catch(function (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err, 60)
          })
      } else {
        this.loadAllData()
      }
    },

    clearSearch: function () {
      if (this.searchText) {
        this.searchText = null
        this.freqFilter = 5
        this.loadAllData()
      }
      this.$refs.searchField.blur()
    },

    filterByFreq: function () {
      this.search()
    },

    _loadBudgetData: function (archivedOnly = false) {
      const self = this

      let query = BudgetDB.QUERIES.UNARCHIVED
      if (archivedOnly) {
        query = BudgetDB.QUERIES.ARCHIVED
      }

      BudgetDB.getEntries(query)
        .then(function (docs) {
          self.budget = docs
          self._loadCategoryData()
        })
        .catch(function (err) {
          self.displayAlert('mdi-alert-octagon', 'red', err, 60)
        })
    },

    _loadCategoryData: function () {
      const self = this

      BudgetDB.getCategories(BudgetDB.QUERIES.UNARCHIVED)
        .then(function (cats) {
          // Set Category List from budget entries
          self.categories = Object.keys(cats)
        })
        .catch(function (err) {
          self.displayAlert('mdi-alert-octagon', 'red', err, 60)
        })
    },

    displayAlert: function (icon, color, message, timeout = 6) {
      this.alert.icon = icon
      this.alert.color = color
      this.alert.message = message
      this.alert.timeout = timeout * 1000
      this.alert.visible = true
    },

    newEntry: function () {
      // this.$refs.iconSelect.focus()
      this.showAddEditSheet = true
    },

    editEntry: function (entry) {
      this.entry = entry
      this.storeHistory()
      this.showAddEditSheet = true
    },

    _clearEntry: function () {
      this.entry = {}
    },

    setView: function (menuItem) {
      this.view = menuItem.id

      if (this.view === Constants.BUDGET_VIEW_ARCHIVED) {
        this._loadBudgetData(true)
      } else {
        this.refreshData()
      }
    },

    storeHistory: function () {
      const self = this

      this.oldEntry = {}
      HISTORY_FIELDS.forEach(function (fld) {
        self.oldEntry[fld] = self.entry[fld]
      })
    },

    updateHistory: function () {
      const self = this

      const promise = new Promise((resolve, reject) => {
        if (this.oldEntry) {
          const historyRec = { date: Date.now() }
          let relevantChange = false
          HISTORY_FIELDS.forEach(function (fld) {
            if (self.entry[fld] !== self.oldEntry[fld]) {
              historyRec[fld] = self.oldEntry[fld]
              relevantChange = true
            }
          })

          if (relevantChange) {
            // Create history list if not exist
            if (!this.entry.history) {
              this.entry.history = []
            }
            this.entry.history.push(historyRec)

            // Show dialog asking for change note
            this.showHistoryNoteDialog = true
            this.historyCallback = resolve
          } else {
            resolve()
          }

          // Zero out for next use
          this.oldEntry = null
        } else {
          resolve()
        }
      })

      return promise
    },

    validateEntry: function (entry) {
      // Ensure private/hidden fields are set
      if (!entry.archivedAt) {
        entry.archivedAt = null
      }
    },

    saveEntry: function () {
      const self = this

      if (this.$refs.budgetForm.validate()) {
        if (!this.entry.icon) {
          const icon = Icons.superSearch(this.entry.category, ':', true)
          this.entry.icon = icon ? icon.value : Icons.ICONS[0].value
        }

        this.entry.amount = parseFloat(this.entry.amount)
        this.entry.type = this.entry.amount > 0 ? Constants.TYPE_INCOME : Constants.TYPE_EXPENSE

        this.validateEntry(this.entry)

        this.updateHistory()
          .then((note) => {
            // History note dialog resolves a promise with the note entered by the user
            if (this.entry.history && note) {
              const index = this.entry.history.length - 1
              // Get last history record (most recent one)
              const history = this.entry.history[index]
              // Add note
              history.note = note

              this.historyCallback = null
              this.historyNote = null
            }

            return BudgetDB.save(this.entry)
          })
          .then(function (numReplaced, upsert) {
            self._clearEntry()
            self.$refs.iconSelect.$el.focus()

            self.refreshData()
            self.displayAlert('mdi-content-save', 'green', 'Entry Successfully Saved')
          })
          .catch(function (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err, 60)
          })
      }
    }
  },

  watch: {
    freqFilter: 'filterByFreq'
  },

  data () {
    return {
      constants: Constants,
      icons: Icons,
      categories: [],
      format: Format,
      searchText: null,
      freqFilter: 5,
      budget: [],
      alert: {
        visible: false,
        icon: 'mdi-alert',
        color: 'green',
        message: '',
        timeout: 10000
      },
      entry: {
        type: null,
        icon: null,
        category: null,
        amount: null,
        firstDue: null,
        frequency: null,
        archivedAt: null,
        notes: null
      },
      // Used to temp. track fields for history purposes
      oldEntry: null,
      historyNote: null,
      historyCallback: null,
      showHistoryNoteDialog: false,
      menu: [
        { name: 'View Active Entries', id: Constants.BUDGET_VIEW_SUMMARY },
        { name: 'View Archived Entries', id: Constants.BUDGET_VIEW_ARCHIVED },
        { name: 'View By Month', id: Constants.BUDGET_VIEW_BYMONTH }
      ],
      view: Constants.BUDGET_VIEW_SUMMARY,
      showAddEditSheet: false,
      rules: {
        category: [
          category => !!category || 'Category is required'
        ],
        amount: [
          amount => !!amount || 'Amount is required',
          amount => (parseFloat(amount) !== 0.0) || 'Amount cannot be zero',
          amount => /^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?$/.test(amount) || 'Amount must be a dollar amount'
        ],
        frequency: [
          freq => !!freq || 'Frequency is required'
        ],
        firstDue: [
          fdue => !!fdue || 'First Due Month is required'
        ]
      }
    }
  }
}
</script>
