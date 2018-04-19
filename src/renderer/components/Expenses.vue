<template>
<div>
    <v-toolbar color="grey darken-2" dark dense app fixed>
      <v-toolbar-title>
        Expenses - {{ currentMonthName }}
      </v-toolbar-title>
      <v-dialog
        ref="monthDialog"
        persistent
        v-model="showMonthDialog"
        lazy
        full-width
        width="290px"
        :return-value.sync="monthToView">
        <v-btn slot="activator" icon color="orange lighten-2"><v-icon>mdi-calendar-range</v-icon></v-btn>
        <v-date-picker
          type="month"
          v-model="monthToView"
          next-icon="mdi-chevron-right"
          prev-icon="mdi-chevron-left"
          color="green accent-3">
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="showMonthDialog = false">Cancel</v-btn>
          <v-btn flat color="primary" @click="$refs.monthDialog.save(monthToView)">OK</v-btn>
        </v-date-picker>
      </v-dialog>
      <v-spacer></v-spacer>
      <v-flex>
        <v-btn-toggle v-model="viewStyle" mandatory class="orange lighten-2">
          <v-btn flat>
            <v-icon>mdi-chart-bar</v-icon>
          </v-btn>
          <v-btn flat>
            <v-icon>mdi-view-list</v-icon>
          </v-btn>
        </v-btn-toggle>
      </v-flex>
      <v-flex>
        <v-toolbar-items>
          <v-chip color="green accent-1" text-color="black" tabindex="-1" disabled>
            <v-icon left>mdi-currency-usd</v-icon>
            <span class="subheading">{{ format.formatMoney(incomeAmount) }}</span>
          </v-chip>
          <v-chip color="red accent-1" text-color="black" tabindex="-1" disabled>
            <v-icon left>mdi-currency-usd-off</v-icon>
            <span class="subheading">{{ format.formatMoney(expensesAmount) }}</span>
          </v-chip>
          <v-chip :color="incomeAmount + expensesAmount >= 0 ? 'green accent-3' : 'red accent-3'" text-color="black" tabindex="-1" disabled>
            <v-icon left>mdi-cash-multiple</v-icon>
            <span class="subheading">{{ format.formatMoney(incomeAmount + expensesAmount) }}</span>
          </v-chip>
          <v-btn-toggle v-model="incomeExpenseView" class="green">
            <v-btn flat>
              <v-icon>mdi-coin</v-icon>
            </v-btn>
          </v-btn-toggle>
        </v-toolbar-items>
      </v-flex>
      <v-flex>
        <v-toolbar-items>
          <v-btn @click="search()" icon color="orange lighten-2"><v-icon>mdi-magnify</v-icon></v-btn>
          &nbsp;
          <v-text-field
            v-model="searchText"
            hide-details
            color="black"
            single-line>
          </v-text-field>
          <v-btn @click="clearSearch()" icon color="grey darken-2"><v-icon>mdi-close</v-icon></v-btn>
        </v-toolbar-items>
      </v-flex>
      <v-spacer></v-spacer>
    </v-toolbar>

    <v-alert
      :color="alert.color"
      v-model="alert.visible"
      :icon="alert.icon"
      class="elevation-24"
      @click="alert.visible=false">
      {{ alert.message }}
    </v-alert>

    <v-list v-if="dataLoaded && viewStyle === constants.VIEW_STYLE_LIST" dense v-for="entry in expenses"
      v-bind:key="entry._id">
      <ExpenseEntry
        v-bind:entry="entry"
        v-on:editEntry="editEntry"
        v-on:refreshData="refreshData"
        v-on:displayAlert="displayAlert">
      </ExpenseEntry>
    </v-list>

    <v-list v-if="dataLoaded && viewStyle === constants.VIEW_STYLE_GROUP" dense v-for="entry in expenses"
      v-bind:key="entry._id">
      <ExpenseCategory
        v-bind:entry="entry">
      </ExpenseCategory>
    </v-list>

    <div class="text-xs-center">
      <v-bottom-sheet v-model="showAddEditSheet">
        <v-btn
          slot="activator"
          color="green accent-3"
          @click="entry = {}"
          fixed bottom right dark fab small>
          <v-icon>mdi-plus</v-icon>
        </v-btn>
        <v-card>
          <v-form ref="expenseForm">
            <v-layout row>
              <v-flex xs3>
                <v-menu
                  ref="dateMenu"
                  lazy
                  :close-on-content-click="false"
                  v-model="showDateMenu"
                  transition="scale-transition"
                  offset-y
                  full-width
                  :nudge-right="40"
                  min-width="290px"
                  :return-value.sync="entryDateStr">
                  <v-text-field
                    slot="activator"
                    label="Date"
                    v-model="entryDateStr"
                    prepend-icon="mdi-calendar-range"
                    readonly
                    required
                  ></v-text-field>
                  <v-date-picker v-model="entryDateStr"
                    next-icon="mdi-chevron-right"
                    prev-icon="mdi-chevron-left"
                    color="green accent-3">
                    <v-spacer></v-spacer>
                    <v-btn flat color="error" @click="showDateMenu = false">Cancel</v-btn>
                    <v-btn color="success" @click="$refs.dateMenu.save(entryDateStr)">OK</v-btn>
                  </v-date-picker>
                </v-menu>
              </v-flex>
              <v-flex xs3>
                <v-select
                  :items="categories"
                  v-model="entry.category"
                  label="Category"
                  single-line
                  dense
                  required
                  :rules="rules.category"
                  combobox
                  tabindex="2"
                  hint="Choose a Category or Add a New One"
                  append-icon="mdi-menu-down">
                </v-select>
              </v-flex>
              <v-flex xs1>
                <v-text-field
                  name="amount"
                  label="Amount"
                  id="amount"
                  tabindex="3"
                  required
                  hint="Positive for Income, Negative for Expense"
                  :rules="rules.amount"
                  v-model="entry.amount">
                </v-text-field>
              </v-flex>
              <v-flex xs4>
                <v-text-field
                  name="notes"
                  label="Notes"
                  id="notes"
                  tabindex="6"
                  v-model="entry.notes">
                </v-text-field>
              </v-flex>
              <v-flex xs1>
                <v-btn color="green accent-3" fab @click="saveEntry()" tabindex="7">
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
import BudgetDB from '../lib/BudgetDB'
import ExpenseEntry from './ExpenseEntry'
import ExpenseCategory from './ExpenseCategory'
import ExpenseDB from '../lib/ExpenseDB'
import Format from '../lib/Format'
import Constants from '../lib/Constants'

export default {
  name: 'Expenses',
  components: { ExpenseEntry, ExpenseCategory },

  mounted () {
    var today = new Date()

    this._loadCategoryData()

    // Setting this value triggers the changeMonth() method below
    this.monthToView = today.getFullYear() + '-' + (today.getMonth() + 1)
  },

  computed: {
    incomeAmount: function () {
      var amount = null

      if (this.incomeExpenseView === Constants.IE_VIEW_TO_DATE) {
        amount = this.incomeExpenseData('toDate', Constants.TYPE_INCOME)
      } else if (this.incomeExpenseView === Constants.IE_VIEW_BUDGETED) {
        amount = this.incomeExpenseData('budgeted', Constants.TYPE_INCOME)
      }

      return (amount)
    },

    expensesAmount: function () {
      var amount = null

      if (this.incomeExpenseView === Constants.IE_VIEW_TO_DATE) {
        amount = this.incomeExpenseData('toDate', Constants.TYPE_EXPENSE)
      } else if (this.incomeExpenseView === Constants.IE_VIEW_BUDGETED) {
        amount = this.incomeExpenseData('budgeted', Constants.TYPE_EXPENSE)
      }

      return (amount)
    }
  },

  methods: {
    incomeExpenseData: function (type, iORe) {
      var value = null

      if (type === 'budgeted') {
        if (iORe === Constants.TYPE_INCOME) {
          value = this.budgetedIncome()
        } else if (iORe === Constants.TYPE_EXPENSE) {
          value = this.budgetedExpenses()
        }
      } else if (type === 'toDate') {
        if (iORe === Constants.TYPE_INCOME) {
          value = this.toDateIncome()
        } else if (iORe === Constants.TYPE_EXPENSE) {
          value = this.toDateExpenses()
        }
      }

      return (value)
    },

    budgetedIncome: function () {
      var amount = 0.0
      Object.values(this.categoriesForMonth).forEach(amt => {
        if (amt > 0.0) {
          amount += amt
        }
      })

      return (amount)
    },

    budgetedExpenses: function () {
      var amount = 0.0
      Object.values(this.categoriesForMonth).forEach(amt => {
        if (amt < 0.0) {
          amount += amt
        }
      })

      return (amount)
    },

    toDateIncome: function () {
      var income = 0.0
      for (var i = 0; i < this.expenses.length; i++) {
        var entry = this.expenses[i]
        var amount = 0.0
        // Grouped (UNBUDGETED) entries
        if (Array.isArray(entry)) {
          entry.forEach(e => { amount += e.amount })
        } else {
          amount = entry.amount
        }

        if (amount >= 0.0) {
          income += amount
        }
      }
      return (income)
    },

    toDateExpenses: function () {
      var expense = 0.0
      for (var i = 0; i < this.expenses.length; i++) {
        var entry = this.expenses[i]
        var amount = 0.0
        // Grouped (UNBUDGETED) entries
        if (Array.isArray(entry)) {
          entry.forEach(e => { amount += e.amount })
        } else {
          amount = entry.amount
        }

        if (amount < 0.0) {
          expense += amount
        }
      }
      return (expense)
    },

    search: function () {
      var self = this

      if (this.searchText) {
        var parts = this.searchText.split(/:/, 2)

        var query = {}
        if (parts.length === 2) {
          query[parts[0].trim()] = new RegExp(parts[1].trim(), 'i')
        } else {
          query['category'] = new RegExp(parts[0].trim(), 'i')
        }

        this.dataLoaded = false
        ExpenseDB.search(this.startDate, this.endDate, query, null, function (err, docs) {
          if (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err)
          } else {
            if (self.viewStyle === Constants.VIEW_STYLE_GROUP) {
              self._groupExpensesData(docs, false)
            } else {
              self.expenses = docs
            }
            self.dataLoaded = true
          }
        })
      }
    },

    clearSearch: function () {
      if (this.searchText) {
        this.searchText = null
        this.refreshData()
      }
    },

    editEntry: function (entry) {
      this.entry = entry
      this.showAddEditSheet = true
    },

    saveEntry: function () {
      var self = this

      if (this.$refs.expenseForm.validate()) {
        if (this.entryDateStr) {
          var parts = this.entryDateStr.split('-', 3)
          parts = parts.map(p => Number.parseInt(p))
          this.entry.date = new Date(parts)
        } else {
          if (!this.entry.date) {
            this.entry.date = new Date()
          }
        }

        this.entry.amount = parseFloat(this.entry.amount)
        this.entry.type = this.entry.amount > 0 ? Constants.TYPE_INCOME : Constants.TYPE_EXPENSE

        ExpenseDB.save(this.entry, function (err, numReplaced, upsert) {
          if (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err)
          } else {
            self._loadExpensesData()
            self.entry = {}
            self.entryDateStr = null

            self.displayAlert('mdi-content-save', 'green', 'Entry Successfully Saved')
          }
        })
      }
    },

    refreshData: function () {
      this._loadExpensesData()
    },

    displayAlert: function (icon, color, message) {
      this.alert.icon = icon
      this.alert.color = color
      this.alert.message = message.toString()
      this.alert.visible = true
    },

    _loadExpensesData: function () {
      var self = this
      this.dataLoaded = false

      var promise = new Promise(function (resolve, reject) {
        ExpenseDB.loadData(self.startDate, self.endDate, function (err, docs) {
          if (err) {
            reject(err)
          } else {
            resolve(docs)
          }
        })
      })

      promise
        .then(function (docs) {
          if (self.viewStyle === Constants.VIEW_STYLE_GROUP) {
            var loadCatData = self._loadCategoryDataByMonth(self.startDate.getMonth())
            loadCatData
              .then(function (cats) {
                self.categoriesForMonth = cats
                self._groupExpensesData(docs)
              })
              // Not sure if this will propagate the error to the catch() below
              .catch(function (err) {
                return (err)
              })
          } else {
            self.expenses = docs
          }
          self.dataLoaded = true
        })
        .catch(function (err) {
          self.displayAlert('mdi-alert-octagon', 'red', err)
        })
    },

    _groupExpensesData: function (entries, seed = true) {
      var groupedEntries = {}
      var newEntries = []

      // Seed with Budget Categories Due for Current Month
      if (seed) {
        Object.keys(this.categoriesForMonth).forEach(function (category) {
          groupedEntries[category] = []
        })
      }

      entries.forEach(function (entry) {
        if (!groupedEntries[entry.category]) {
          groupedEntries[entry.category] = []
        }
        groupedEntries[entry.category].push(entry)
      })

      var unbudgtedEntries = []
      Object.entries(groupedEntries).forEach(([cat, catEntries]) => {
        var totalAmount = 0.0
        var budgetedAmount = this.categoriesForMonth[cat] || 0.0
        var type = budgetedAmount > 0.0 ? Constants.TYPE_INCOME : Constants.TYPE_EXPENSE

        if (catEntries.length > 0) {
          catEntries.forEach(function (entry) {
            totalAmount += entry.amount
          })
        }

        var newEntry = {type: type, category: cat, amount: totalAmount, budgetedAmount: budgetedAmount}

        if (cat.startsWith('UNBUDGETED')) {
          unbudgtedEntries.push(newEntry)
        } else {
          newEntries.push(newEntry)
        }
      })

      newEntries.push(unbudgtedEntries)

      this.expenses = newEntries
    },

    _loadCategoryData: function () {
      var self = this
      BudgetDB.loadCategories(function (err, cats) {
        if (err) {
          self.displayAlert('mdi-alert-octagon', 'red', err)
        } else {
          // Set Category List from budget entries
          self.categories = cats.concat(['UNBUDGETED'])
        }
      })
    },

    _loadCategoryDataByMonth: function (month) {
      var promise = new Promise(function (resolve, reject) {
        BudgetDB.loadCategoryDataByMonth(month, function (err, cats) {
          if (err) {
            reject(err)
          } else {
            resolve(cats)
          }
        })
      })

      return (promise)
    },

    viewStyleChange: function () {
      if (this.searchText) {
        this.search()
      } else {
        this.refreshData()
      }
    },

    changeMonth: function () {
      var parts = this.monthToView.split('-', 2).map(p => Number.parseInt(p))

      this.startDate = new Date(parts[0], parts[1] - 1, 1)
      this.endDate = new Date(parts[0], parts[1], 0)
      this.currentMonthName = Format.monthNumberToName(this.startDate.getMonth())

      // console.log('S: ' + this.startDate)
      // console.log('E: ' + this.endDate)
      // console.log('N: ' + this.currentMonthName)
      this.refreshData()
    }

  },

  watch: {
    viewStyle: 'viewStyleChange',
    monthToView: 'changeMonth'
  },

  data () {
    return {
      constants: Constants,
      categoriesForMonth: null,
      categories: [],
      format: Format,
      viewStyle: Constants.VIEW_STYLE_GROUP,
      incomeExpenseView: Constants.IE_VIEW_TO_DATE,
      expenses: [],
      dataLoaded: false,
      searchText: null,
      monthToView: null,
      currentMonthName: null,
      startDate: null,
      endDate: null,
      showMonthDialog: false,
      alert: {
        visible: false,
        icon: 'mdi-alert',
        color: 'green',
        message: ''
      },
      entryDateStr: null,
      entry: {
        type: null,
        date: null,
        category: null,
        amount: null,
        notes: null
      },
      showDateMenu: false,
      showAddEditSheet: false,
      rules: {
        date: [
          date => !!date || 'Date is required'
        ],
        category: [
          category => !!category || 'Category is required'
        ],
        amount: [
          amount => !!amount || 'Amount is required',
          amount => (parseFloat(amount) !== 0.0) || 'Amount cannot be zero',
          amount => /^[+-]?[0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})?$/.test(amount) || 'Amount must be a dollar amount'
        ]
      }
    }
  }
}
</script>
