<template>
  <div>
    <v-app-bar :color="constants.COLORS.TOOLBAR" app dark dense fixed>
      <v-menu bottom offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item v-for="(item, i) in menu" :key="i" @click="setView(item)">
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-toolbar-title id="budget-toolbar-title">Budget</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-flex>
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
      </v-flex>
      <v-flex>
        <v-toolbar-items>
          <v-chip :color="constants.COLORS.INCOME" text-color="black">
            <v-icon float-left>mdi-currency-usd</v-icon>
            <span class="subtitle-1">{{ format.formatMoney(totalIncome) }}</span>
          </v-chip>&nbsp;
          <v-chip :color="constants.COLORS.EXPENSE" text-color="black">
            <v-icon float-left>mdi-currency-usd-off</v-icon>
            <span class="subtitle-1">{{ format.formatMoney(totalExpenses) }}</span>
          </v-chip>&nbsp;
          <v-chip
            :color="totalIncome + totalExpenses >= 0 ? constants.COLORS.INCOME_ALT : constants.COLORS.EXPENSE_ALT"
            text-color="black"
          >
            <v-icon float-left>mdi-cash-multiple</v-icon>
            <span class="subtitle-1">{{ format.formatMoney(totalIncome + totalExpenses) }}</span>
          </v-chip>
        </v-toolbar-items>
      </v-flex>
      <v-flex>
        <v-toolbar-items>
          <v-btn @click="search()" icon small :color="constants.COLORS.TOOLBAR_BUTTON">
            <v-icon>mdi-magnify</v-icon>
          </v-btn>&nbsp;
          <v-text-field
            ref="searchField"
            v-model="searchText"
            hide-details
            color="black"
            single-line
            @keyup.enter="search()"
            @keyup.esc="clearSearch()"
          ></v-text-field>
          <v-btn @click="clearSearch()" icon small :color="constants.COLORS.TOOLBAR_BUTTON">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar-items>
      </v-flex>
    </v-app-bar>

    <v-snackbar bottom v-model="alert.visible" :color="alert.color" :timeout="alert.timeout">
      <v-icon>{{ alert.icon }}</v-icon>
      &nbsp;{{ alert.message }}
      <v-btn icon dark @click="alert.visible=false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-snackbar>

    <template
      v-if="view === constants.BUDGET_VIEW_SUMMARY || view === constants.BUDGET_VIEW_ARCHIVED"
    >
      <v-list dense>
        <BudgetEntry
          v-for="(entry, index) in budget"
          :key="index"
          v-bind:entryNum="index"
          v-bind:entry="entry"
          v-bind:readOnly="view === constants.BUDGET_VIEW_ARCHIVED ? true : false"
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
            <v-layout>
              <v-flex xs1>
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
              </v-flex>
              <v-flex xs2>
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
              </v-flex>
              <v-flex xs1>
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
              </v-flex>
              <v-flex xs2>
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
              </v-flex>
              <v-flex xs2>
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
              </v-flex>
              <v-flex xs3>
                <v-text-field
                  name="notes"
                  label="Notes"
                  id="notes"
                  v-model="entry.notes"
                  single-line
                  dense
                ></v-text-field>
              </v-flex>
              <v-flex xs1 text-center>
                <v-btn :color="constants.COLORS.OK_BUTTON" fab small @click="saveEntry()">
                  <v-icon>mdi-content-save</v-icon>
                </v-btn>
              </v-flex>
            </v-layout>
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
      var income = 0.0
      for (var i = 0; i < this.budget.length; i++) {
        var entry = this.budget[i]
        if (entry.amount >= 0.0) {
          income += entry.amount
        }
      }
      return (income)
    },

    totalExpenses: function () {
      var expense = 0.0
      for (var i = 0; i < this.budget.length; i++) {
        var entry = this.budget[i]
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
      var self = this
      var terms = []

      var freq = null
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
        terms.push({frequency: freq})
      }

      if (this.searchText) {
        var parts = this.searchText.split(/\?/, 2)

        if (parts.length === 2) {
          var fieldQuery = {}
          fieldQuery[parts[0].trim()] = new RegExp(parts[1].trim(), 'i')

          terms.push(fieldQuery)
        } else {
          terms.push({category: new RegExp(parts[0].trim(), 'i')})
        }
      }

      if (terms.length !== 0) {
        terms.push({archivedAt: null})
        var query = { $and: terms }

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
      var self = this

      var query = BudgetDB.QUERIES.UNARCHIVED
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
      var self = this

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
      var self = this

      this.oldEntry = {}
      HISTORY_FIELDS.forEach(function (fld) {
        self.oldEntry[fld] = self.entry[fld]
      })
    },

    updateHistory: function () {
      var self = this
      var historyRec = { date: Date.now() }
      var relevantChange = false

      if (this.oldEntry) {
        HISTORY_FIELDS.forEach(function (fld) {
          if (self.entry[fld] !== self.oldEntry[fld]) {
            historyRec[fld] = self.oldEntry[fld]
            relevantChange = true
          }
        })
      }

      // Zero out for next use
      this.oldEntry = null

      if (relevantChange) {
        // Create history list if not exist
        if (!this.entry.history) {
          this.entry.history = []
        }

        this.entry.history.push(historyRec)
      }
    },

    validateEntry: function (entry) {
      // Ensure private/hidden fields are set
      if (!entry.archivedAt) {
        entry.archivedAt = null
      }
    },

    saveEntry: function () {
      var self = this

      if (this.$refs.budgetForm.validate()) {
        if (!this.entry.icon) {
          var icon = Icons.superSearch(this.entry.category, ':', true)
          this.entry.icon = icon ? icon.value : Icons.ICONS[0].value
        }

        this.entry.amount = parseFloat(this.entry.amount)
        this.entry.type = this.entry.amount > 0 ? Constants.TYPE_INCOME : Constants.TYPE_EXPENSE

        this.validateEntry(this.entry)

        this.updateHistory()

        BudgetDB.save(this.entry)
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
      menu: [
        {name: 'View Active Entries', id: Constants.BUDGET_VIEW_SUMMARY},
        {name: 'View Archived Entries', id: Constants.BUDGET_VIEW_ARCHIVED},
        {name: 'View By Month', id: Constants.BUDGET_VIEW_BYMONTH}
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
