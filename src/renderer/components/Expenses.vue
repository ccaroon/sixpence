<template>
<div>

    <v-toolbar color="grey darken-2" dark dense app fixed>
      <v-menu bottom offset-y>
        <v-btn slot="activator" icon>
          <v-icon>mdi-menu</v-icon>
        </v-btn>
        <v-list dense>
          <v-list-tile @click="viewOverbudgetEntries()">
            <v-list-tile-title>{{ menu.viewOverbudgetEntries.labels[menu.viewOverbudgetEntries.labelIndex] }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
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
            ref="searchField"
            v-model="searchText"
            hide-details
            color="black"
            single-line
            @keyup.enter="search()"
            @keyup.esc="clearSearch()">
          </v-text-field>
          <v-btn @click="clearSearch()" icon color="grey darken-2"><v-icon>mdi-close</v-icon></v-btn>
        </v-toolbar-items>
      </v-flex>
      <v-spacer></v-spacer>
    </v-toolbar>

    <v-snackbar
      bottom
      v-model="alert.visible"
      :color="alert.color"
      :timeout="alert.timeout">
      <v-icon>{{ alert.icon }}</v-icon>
      &nbsp;{{ alert.message }}
      <v-btn icon dark @click="alert.visible=false"><v-icon>mdi-close</v-icon></v-btn>
    </v-snackbar>

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
        v-bind:entry="entry"
        v-on:viewEntriesInGroup="viewEntriesInGroup">
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
              <v-flex xs2>
                <v-text-field
                  label="Date"
                  v-model="entryDateStr"
                  prepend-icon="mdi-calendar-range"
                  required
                  :rules="rules.date">
                </v-text-field>
              </v-flex>
              <v-flex xs3>
                <v-select
                  ref="categorySelect"
                  :items="categories"
                  v-model="entry.category"
                  label="Category"
                  single-line
                  dense
                  required
                  :rules="rules.category"
                  combobox
                  hint="Choose a Category or Add a New One"
                  append-icon="mdi-menu-down">
                </v-select>
              </v-flex>
              <v-flex xs1>
                <v-text-field
                  name="amount"
                  label="Amount"
                  id="amount"
                  required
                  hint="Positive for Income, Negative for Expense"
                  :rules="rules.amount"
                  v-model="entry.amount">
                </v-text-field>
              </v-flex>
              <v-flex xs5>
                <v-text-field
                  name="notes"
                  label="Notes"
                  id="notes"
                  v-model="entry.notes">
                </v-text-field>
              </v-flex>
              <v-flex xs1>
                <v-btn color="green accent-3" fab @click="saveEntry()">
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
import Mousetrap from 'Mousetrap'
import Moment from 'moment'

export default {
  name: 'Expenses',
  components: { ExpenseEntry, ExpenseCategory },

  mounted () {
    var self = this
    var today = new Date()

    this._bindShortcutKeys()

    ExpenseDB.ensureRollover(today.getMonth() + 1)
      .then(function () {
        // Setting this value triggers the changeMonth() method below
        self.monthToView = today.getFullYear() + '-' + (today.getMonth() + 1)
      })
      .then(function () {
        self._loadCategoryData()
      })
      .catch(function (err) {
        self.displayAlert('mdi-alert-octagon', 'red', err, 60)
      })
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
        // Grouped Unbudgeted entries
        if (Array.isArray(entry)) {
          entry.forEach(e => {
            if (e.amount >= 0.0) {
              amount += e.amount
            }
          })
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
        // Grouped Unbudgeted entries
        if (Array.isArray(entry)) {
          entry.forEach(e => {
            if (e.amount < 0.0) {
              amount += e.amount
            }
          })
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
        var parts = this.searchText.split(/\?/, 2)

        var query = {}
        if (parts.length === 2) {
          query[parts[0].trim()] = new RegExp(parts[1].trim(), 'i')
        } else {
          query['category'] = new RegExp(parts[0].trim(), 'i')
        }

        this.dataLoaded = false
        ExpenseDB.search(this.startDate, this.endDate, query, null, function (err, docs) {
          if (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err, 60)
          } else {
            if (self.viewStyle === Constants.VIEW_STYLE_GROUP) {
              self._groupExpensesData(docs, false)
            } else {
              self.expenses = docs
            }
            self.dataLoaded = true
          }
        })
      } else {
        this.loadAllData()
      }
    },

    clearSearch: function () {
      if (this.searchText) {
        this.searchText = null
        this.loadAllData()
      }
      this.$refs.searchField.blur()
    },

    newEntry: function () {
      this.entryDateStr = Format.formatDate(new Date(), Constants.FORMATS.entryDate)
      this.$refs.categorySelect.$el.focus()
      this.showAddEditSheet = true
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

        this.entry.icon = this.findIcon(this.entry)
        this.entry.amount = parseFloat(this.entry.amount)

        // IF entry.category IS a budgeted category
        //   use the budgeted category's type for entry.type
        // ELSE
        //   decide type based on > 0.0
        BudgetDB.categoryType(this.entry.category)
          .then(function (type) {
            if (type === null) {
              // category not found
              self.entry.type = self.entry.amount > 0.0 ? Constants.TYPE_INCOME : Constants.TYPE_EXPENSE
            } else {
              self.entry.type = type
              self.entry.amount = Math.abs(self.entry.amount)
              if (type === Constants.TYPE_EXPENSE) {
                self.entry.amount *= -1
              }
            }
          })
          .catch(function (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err, 60)
          })

        ExpenseDB.save(this.entry, function (err, numReplaced, upsert) {
          if (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err, 60)
          } else {
            self.entry = {}
            self.entryDateStr = null

            self.refreshData()
            self.displayAlert('mdi-content-save', 'green', 'Entry Successfully Saved')
          }
        })
      }
    },

    refreshData: function () {
      this.search()
    },

    loadAllData: function () {
      this._loadExpensesData()
    },

    findIcon: function (entry) {
      var icon = this.iconMap[entry.category]

      if (icon === undefined) {
        var parts = entry.category.split(':')
        parts.reverse()

        var foundIcon = null
        for (var i = 0; i < parts.length; i++) {
          var catPart = parts[i]
          var catPattern = new RegExp(catPart, 'i')

          foundIcon = Constants.ICONS.find(function (iconData) {
            if (iconData.text.match(catPattern)) {
              return true
            } else {
              var foundInKw = false
              for (var j = 0; j < iconData.keywords.length; j++) {
                var keyword = iconData.keywords[j]
                if (keyword.match(catPattern)) {
                  foundInKw = true
                  break
                }
              }
              return foundInKw
            }
          })

          if (foundIcon) {
            break
          }
        }

        icon = foundIcon ? foundIcon.value : 'mdi-currency-usd'
      }

      return (icon)
    },

    displayAlert: function (icon, color, message, timeout = 6) {
      this.alert.icon = icon
      this.alert.color = color
      this.alert.message = message.toString()
      this.alert.timeout = timeout * 1000
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
            self._loadCategoryDataByMonth(self.startDate.getMonth())
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
          self.displayAlert('mdi-alert-octagon', 'red', err, 60)
        })
    },

    _groupExpensesData: function (entries, seed = true) {
      var self = this
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
      var budgetCategories = Object.keys(this.categoriesForMonth)
      Object.entries(groupedEntries).forEach(([cat, catEntries]) => {
        var totalAmount = 0.0
        var budgetedAmount = this.categoriesForMonth[cat] || 0.0
        var type = budgetedAmount >= 0.0 ? Constants.TYPE_INCOME : Constants.TYPE_EXPENSE

        var icon = 'mdi-coin'
        if (catEntries.length > 0) {
          icon = catEntries[0].icon
          catEntries.forEach(function (entry) {
            totalAmount += entry.amount
          })
        }

        var newEntry = {type: type, icon: icon, category: cat, amount: totalAmount, budgetedAmount: budgetedAmount}

        if (budgetCategories.includes(newEntry.category)) {
          if (self.showOverbudget) {
            if (Math.abs(newEntry.amount) > Math.abs(newEntry.budgetedAmount)) {
              newEntries.push(newEntry)
            }
          } else {
            newEntries.push(newEntry)
          }
        } else {
          // Since it's unbudgeted, we can't decide the type based on +/- so instead
          // we'll use the type of the first entry in the list of entries
          newEntry.type = catEntries[0].type
          unbudgtedEntries.push(newEntry)
        }
      })

      newEntries.push(unbudgtedEntries)

      this.expenses = newEntries
    },

    _loadCategoryData: function () {
      var self = this

      // Load Categories (includes icons)
      var loadBudgetCats = new Promise(function (resolve, reject) {
        BudgetDB.loadCategories(function (err, cats) {
          if (err) {
            reject(err)
          } else {
            // Mapping from Category name to Icon
            self.iconMap = cats

            // Set Category List from budget entries
            self.categories = Object.keys(cats)

            // Don't care about the resolve value since were setting values on 'self'
            resolve(true)
          }
        })
      })

      // Load Categories used for the current month
      // The point being to get a list of the categories used for Unbudgeted
      // entries and make them available for re-use.
      var loadExpCats = new Promise(function (resolve, reject) {
        ExpenseDB.loadCategories(self.startDate, self.endDate, function (err, cats) {
          if (err) {
            reject(err)
          } else {
            var catNames = cats.map(obj => obj.category)
            var allCats = self.categories.concat(catNames).sort()

            // Filter out dups
            self.categories = [...new Set(allCats)]

            // Don't care about the resolve value since were setting values on 'self'
            resolve(true)
          }
        })
      })

      Promise.all([loadBudgetCats, loadExpCats])
        // .then(function (values) {})
        .catch(function (err) {
          self.displayAlert('mdi-alert-octagon', 'red', err, 60)
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
      this.endDate = new Date(parts[0], parts[1], 0, 23, 59, 59)
      this.currentMonthName = Format.monthNumberToName(this.startDate.getMonth())

      this.refreshData()
    },

    // This is called from ExpenseCategory when the user clicks on the grouped
    // expense category name
    viewEntriesInGroup: function (category) {
      this.searchText = category
      this.viewStyle = Constants.VIEW_STYLE_LIST
      // this.search()
    },

    viewOverbudgetEntries: function () {
      this.showOverbudget = !this.showOverbudget

      if (this.showOverbudget) {
        this.menu.viewOverbudgetEntries.labelIndex = 1
      } else {
        this.menu.viewOverbudgetEntries.labelIndex = 0
      }

      if (this.viewStyle !== Constants.VIEW_STYLE_GROUP) {
        this.viewStyle = Constants.VIEW_STYLE_GROUP
      } else {
        this.refreshData()
      }
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
      iconMap: {},
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
      menu: {
        viewOverbudgetEntries: {
          labels: ['View Overbudget Categories', 'View All Categories'],
          labelIndex: 0
        }
      },
      alert: {
        visible: false,
        icon: 'mdi-alert',
        color: 'green',
        message: '',
        timeout: 10000
      },
      entryDateStr: null,
      entry: {
        type: null,
        date: null,
        icon: null,
        category: null,
        amount: null,
        notes: null
      },
      showDateMenu: false,
      showAddEditSheet: false,
      showOverbudget: false,
      rules: {
        date: [
          date => !!date || 'Date is required',
          date => (Moment(date, Constants.FORMATS.entryDate, true).isValid()) || 'Format as ' + Constants.FORMATS.entryDate
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
