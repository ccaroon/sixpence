<template>
  <div>
    <v-app-bar :color="constants.COLORS.TOOLBAR" dark dense app fixed>
      <v-menu bottom offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item @click="viewOverbudgetEntries()" :disabled="viewingAll">
            <v-list-item-title>{{
              menu.viewOverbudgetEntries.labels[
                menu.viewOverbudgetEntries.labelIndex
              ]
            }}</v-list-item-title>
          </v-list-item>
          <v-list-item @click="recalculateRollover()">
            <v-list-item-title>{{
              menu.recalculateRollover.labels[
                menu.recalculateRollover.labelIndex
              ]
            }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-row no-gutters align="center">
        <v-col cols="1">
          <v-toolbar-title>Expenses</v-toolbar-title>
        </v-col>
        <v-col cols="2">
          <v-dialog
            ref="monthDialog"
            persistent
            v-model="showMonthDialog"
            width="290px"
            :return-value.sync="monthToView"
          >
            <template v-slot:activator="{ on }">
              <v-btn
                tabindex="-1"
                v-on="on"
                outlined
                rounded
                :color="constants.COLORS.TOOLBAR_BUTTON"
              >
                {{ currentMonthName }}
                <v-icon>mdi-calendar-range</v-icon>
              </v-btn>
            </template>

            <v-date-picker
              type="month"
              v-model="monthToView"
              next-icon="mdi-chevron-right"
              prev-icon="mdi-chevron-left"
              :color="constants.COLORS.OK_BUTTON"
            >
              <v-spacer></v-spacer>
              <v-btn
                tabindex="-1"
                text
                color="primary"
                @click="showMonthDialog = false"
                >Cancel</v-btn
              >
              <v-btn
                tabindex="-1"
                text
                color="primary"
                @click="$refs.monthDialog.save(monthToView)"
                >OK</v-btn
              >
            </v-date-picker>
          </v-dialog>
        </v-col>
        <v-col cols="1">
          <v-toolbar-items>
            <v-btn-toggle
              v-model="viewStyle"
              mandatory
              rounded
              :class="constants.COLORS.TOOLBAR_BUTTON"
            >
              <v-btn tabindex="-1" text :disabled="viewingAll">
                <v-icon>mdi-chart-bar</v-icon>
              </v-btn>
              <v-btn tabindex="-1" text>
                <v-icon>mdi-view-list</v-icon>
              </v-btn>
            </v-btn-toggle>
          </v-toolbar-items>
        </v-col>
        <v-col cols="4">
          <v-toolbar-items>
            <v-chip :color="constants.COLORS.INCOME" text-color="black">
              <v-icon float-left>mdi-currency-usd</v-icon>
              <span class="subtitle-1">{{
                format.formatMoney(incomeAmount)
              }}</span> </v-chip
            >&nbsp;
            <v-chip :color="constants.COLORS.EXPENSE" text-color="black">
              <v-icon float-left>mdi-currency-usd-off</v-icon>
              <span class="subtitle-1">{{
                format.formatMoney(expensesAmount)
              }}</span> </v-chip
            >&nbsp;
            <v-chip
              :color="
                incomeAmount + expensesAmount >= 0
                  ? constants.COLORS.INCOME_ALT
                  : constants.COLORS.EXPENSE_ALT
              "
              text-color="black"
            >
              <v-icon float-left>mdi-cash-multiple</v-icon>
              <span class="subtitle-1">{{
                format.formatMoney(incomeAmount + expensesAmount)
              }}</span> </v-chip
            >&nbsp;
          </v-toolbar-items>
        </v-col>
        <v-col cols="1">
          <v-toolbar-items>
            <v-btn-toggle
              tabindex="-1"
              v-model="incomeExpenseView"
              class="green"
            >
              <v-btn tabindex="-1" small icon>
                <v-icon v-if="incomeExpenseView == constants.IE_VIEW_TO_DATE"
                  >mdi-currency-usd</v-icon
                >
                <v-icon v-else>mdi-currency-usd-off</v-icon>
              </v-btn>
            </v-btn-toggle>
          </v-toolbar-items>
        </v-col>
        <v-col>
          <v-toolbar-items>
            <v-btn
              tabindex="-1"
              @click="search()"
              icon
              small
              :color="constants.COLORS.TOOLBAR_BUTTON"
            >
              <v-icon>mdi-magnify</v-icon> </v-btn
            >&nbsp;
            <v-text-field
              tabindex="-1"
              ref="searchField"
              v-model="searchText"
              hide-details
              color="black"
              single-line
              @keyup.enter="search()"
              @keyup.esc="clearSearch()"
            ></v-text-field>
            <v-btn
              tabindex="-1"
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

    <template v-if="dataLoaded && viewStyle === constants.VIEW_STYLE_LIST">
      <v-list dense>
        <ExpenseEntry
          v-for="(entry, index) in expenses"
          :key="index"
          tabindex="-1"
          v-bind:entryNum="index"
          v-bind:entry="entry"
          v-on:editEntry="editEntry"
          v-on:search="search"
          v-on:refreshData="refreshData"
          v-on:displayAlert="displayAlert"
        ></ExpenseEntry>
      </v-list>
    </template>

    <template v-if="dataLoaded && viewStyle === constants.VIEW_STYLE_GROUP">
      <v-list dense>
        <ExpenseCategory
          v-for="(entry, index) in expenses"
          :key="index"
          tabindex="-1"
          v-bind:entryNum="index"
          v-bind:entry="entry"
          v-on:viewEntriesInGroup="viewEntriesInGroup"
        ></ExpenseCategory>
      </v-list>
    </template>

    <div class="text-center">
      <v-bottom-sheet v-model="showAddEditSheet">
        <template v-slot:activator="{ on }">
          <v-btn
            tabindex="-1"
            v-on="on"
            :color="constants.COLORS.OK_BUTTON"
            @click="entry = {}"
            fixed
            bottom
            dark
            fab
            small
            right
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-form ref="expenseForm">
            <v-row no-gutters>
              <v-col cols="2">
                <v-menu
                  tabindex="-1"
                  :close-on-content-click="false"
                  v-model="showDateMenu"
                  :nudge-right="40"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      tabindex="-1"
                      ref="dateField"
                      v-on="on"
                      v-model="entryDateStr"
                      label="Date"
                      prepend-icon="mdi-calendar-range"
                      readonly
                      single-line
                      dense
                      :background-color="newEntryColor()"
                      required
                      :rules="rules.date"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="entryDateStr"
                    @input="showDateMenu = false"
                    :color="constants.COLORS.OK_BUTTON"
                    next-icon="mdi-chevron-right"
                    prev-icon="mdi-chevron-left"
                  ></v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="3">
                <v-combobox
                  tabindex="0"
                  ref="categorySelect"
                  :items="categories"
                  v-model="entry.category"
                  label="Category"
                  single-line
                  dense
                  required
                  :background-color="newEntryColor()"
                  :rules="rules.category"
                  hint="Choose a Category or Add a New One"
                  append-icon="mdi-menu-down"
                  @change="loadCategoryTags()"
                ></v-combobox>
              </v-col>
              <v-col cols="1">
                <v-text-field
                  tabindex="0"
                  name="amount"
                  label="Amount"
                  id="amount"
                  required
                  single-line
                  dense
                  :background-color="newEntryColor()"
                  hint="+/- Amount"
                  :rules="rules.amount"
                  v-model="entry.amount"
                  :placeholder="amountPlaceholder"
                ></v-text-field>
              </v-col>
              <v-col cols="5">
                <v-combobox
                  v-model="entry.tags"
                  :items="this.tagList"
                  :background-color="newEntryColor()"
                  label="Tags"
                  multiple
                  single-line
                  dense
                >
                  <template
                    v-slot:selection="{ attrs, item, select, selected }"
                  >
                    <v-chip
                      v-bind="attrs"
                      :input-value="selected"
                      close
                      :color="newEntryColor('tag')"
                      small
                      @click="select"
                      @click:close="removeTag(item)"
                      >{{ item }}</v-chip
                    >
                  </template>
                </v-combobox>
              </v-col>
              <v-col cols="1" text-center>
                <v-btn
                  tabindex="0"
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
import BudgetDB from '../lib/BudgetDB'
import Constants from '../lib/Constants'
import ExpenseEntry from './Expense/Entry'
import ExpenseCategory from './Expense/Category'
import ExpenseDB from '../lib/ExpenseDB'
import Format from '../lib/Format'
import Icons from '../lib/Icons'
import Mousetrap from 'mousetrap'
import Moment from 'moment'

export default {
  name: 'Expenses',
  components: { ExpenseEntry, ExpenseCategory },

  mounted () {
    const self = this
    const today = new Moment()

    this._bindShortcutKeys()

    ExpenseDB.ensureRollover(today.month())
      .then(function () {
        const startMonth = new Moment()

        if (self.$route.params) {
          if (self.$route.params.category) {
            self.searchText = self.$route.params.category
            self.viewStyle = Constants.VIEW_STYLE_LIST
            self.viewingAll = true

            self.startDate = null
            self.endDate = null
            self.currentMonthName = 'All'

            self.refreshData()
          } else if (self.$route.params.month) {
            // Setting `monthToView` triggers the changeMonth() method below
            self.monthToView = startMonth.month(self.$route.params.month).format('YYYY-MM')
          } else {
            self.monthToView = startMonth.format('YYYY-MM')
          }
        } else {
          self.monthToView = startMonth.format('YYYY-MM')
        }
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
      let amount = null

      if (this.incomeExpenseView === Constants.IE_VIEW_TO_DATE) {
        amount = this.incomeExpenseData('toDate', Constants.TYPE_INCOME)
      } else if (this.incomeExpenseView === Constants.IE_VIEW_BUDGETED) {
        amount = this.incomeExpenseData('budgeted', Constants.TYPE_INCOME)
      }

      return (amount)
    },

    expensesAmount: function () {
      let amount = null

      if (this.incomeExpenseView === Constants.IE_VIEW_TO_DATE) {
        amount = this.incomeExpenseData('toDate', Constants.TYPE_EXPENSE)
      } else if (this.incomeExpenseView === Constants.IE_VIEW_BUDGETED) {
        amount = this.incomeExpenseData('budgeted', Constants.TYPE_EXPENSE)
      }

      return (amount)
    },

    amountPlaceholder: function () {
      let value = ''

      if (this.categoriesForMonth && this.categoriesForMonth[this.entry.category]) {
        value = this.categoriesForMonth[this.entry.category].toString()
      }

      return (value)
    }
  },

  methods: {
    _bindShortcutKeys: function () {
      const self = this

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
        this.entryDateStr = null
        return false
      })

      Mousetrap.bind('+', () => {
        if (self.showAddEditSheet && self.entryDateStr) {
          self._deltaEntryDate(1, 'days')
        }
        return false
      })

      Mousetrap.bind('=', () => {
        if (self.showAddEditSheet && self.entryDateStr) {
          self._deltaEntryDate(1, 'days')
        }
        return false
      })

      Mousetrap.bind('-', () => {
        if (self.showAddEditSheet && self.entryDateStr) {
          self._deltaEntryDate(-1, 'days')
        }
        return false
      })
    },

    incomeExpenseData: function (type, iORe) {
      let value = null

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
      let amount = 0.0
      Object.values(this.categoriesForMonth).forEach(amt => {
        if (amt > 0.0) {
          amount += amt
        }
      })

      return (amount)
    },

    budgetedExpenses: function () {
      let amount = 0.0
      Object.values(this.categoriesForMonth).forEach(amt => {
        if (amt < 0.0) {
          amount += amt
        }
      })

      return (amount)
    },

    toDateIncome: function () {
      let income = 0.0
      for (let i = 0; i < this.expenses.length; i++) {
        const entry = this.expenses[i]
        let amount = 0.0
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
      let expense = 0.0
      for (let i = 0; i < this.expenses.length; i++) {
        const entry = this.expenses[i]
        let amount = 0.0
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

    loadCategoryTags: async function () {
      const self = this
      this.tagList = []

      if (this.entry.category) {
        try {
          // Find all Tags used for the category in the lasts 6 months
          const startDate = Moment(this.endDate).subtract(6, 'months')
          const endDate = this.endDate

          const docs = await ExpenseDB.search(startDate, endDate, { category: this.entry.category }, {}, { tags: 1 })

          let catTags = []
          docs.forEach(entry => {
            if (entry.tags) {
              catTags = catTags.concat(entry.tags)
            }
          })

          // Use a Set to de-dup list
          // & convert back into Array
          this.tagList = [...new Set(catTags)]
        } catch (err) {
          self.displayAlert('mdi-alert-octagon', 'red', err, 60)
        }
      }
    },

    newEntryColor: function (type = 'base') {
      let color = Constants.COLORS.GREY
      let incColor = Constants.COLORS.INCOME_ALT
      let expColor = Constants.COLORS.EXPENSE_ALT

      if (type === 'tag') {
        color = Constants.COLORS.GREY_ALT
        incColor = Constants.COLORS.INCOME
        expColor = Constants.COLORS.EXPENSE
      }

      if (this.categoriesForMonth && this.categoriesForMonth[this.entry.category]) {
        color = this.categoriesForMonth[this.entry.category] > 0 ? incColor : expColor
      } else if (this.entry.amount) {
        if (this.entry.amount < 0) {
          color = expColor
        } else if (this.entry.amount > 0) {
          color = incColor
        }
      }

      return (color)
    },

    search: function (searchFor = null) {
      const self = this

      if (searchFor !== null) {
        this.searchText = searchFor
      }

      if (this.searchText) {
        const parts = this.searchText.split(/\?/, 2)

        let query = {}
        if (parts.length === 2) {
          query[parts[0].trim()] = new RegExp(parts[1].trim(), 'i')
        } else {
          const term = new RegExp(parts[0].trim(), 'i')
          query = {
            $or: [
              { category: term },
              { tags: term }
            ]
          }
        }

        this.dataLoaded = false
        ExpenseDB.search(this.startDate, this.endDate, query)
          .then(function (docs) {
            if (self.viewStyle === Constants.VIEW_STYLE_GROUP) {
              self._groupExpensesData(docs, false)
            } else {
              self.expenses = docs
            }
            self.dataLoaded = true
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
        this.loadAllData()
      }
      this.$refs.searchField.blur()
    },

    newEntry: function () {
      this.entryDateStr = Format.formatDate(new Date(), Constants.FORMATS.entryDate)
      // this.$refs.categorySelect.$el.focus()
      // this.$refs.dateField.focus()
      this.showAddEditSheet = true
    },

    editEntry: function (entry) {
      this.entry = entry

      this.loadCategoryTags()
      this.entryDateStr = Format.formatDate(this.entry.date, Constants.FORMATS.entryDate)

      this.showAddEditSheet = true
    },

    saveEntry: function () {
      const self = this

      if (this.$refs.expenseForm.validate()) {
        if (this.entryDateStr) {
          this.entry.date = Moment(this.entryDateStr, Constants.FORMATS.entryDate, true).toDate()
        } else {
          if (!this.entry.date) {
            this.entry.date = new Date()
          }
        }

        this.entry.icon = this.findIcon(this.entry)
        this.entry.amount = parseFloat(this.entry.amount)

        if (this.entry.tags) {
          delete this.entry.notes
          this.entry.tags.sort()
        }

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

        ExpenseDB.save(this.entry)
          .then(function (numReplaced, upsert) {
            self.entry = {}
            self.entryDateStr = null

            self.refreshData()
            self.displayAlert('mdi-content-save', 'green', 'Entry Successfully Saved')
          })
          .catch(function (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err, 60)
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
      let foundIcon = null

      // Find exact match to category
      let icon = this.iconMap[entry.category]

      // Find match by breaking category down into parts based on ':' divider
      // with rightmost parts matched first
      if (icon === undefined) {
        foundIcon = Icons.superSearch(entry.category, ':', true)
        icon = foundIcon ? foundIcon.value : undefined
      }

      // Try to find a match from the list of tags
      // "Dentist", "Food", "..."
      if (icon === undefined) {
        foundIcon = Icons.superSearch(entry.tags)
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

    _deltaEntryDate: function (amount, units) {
      const entryDate = Moment(this.entryDateStr, Constants.FORMATS.entryDate)
      entryDate.add(amount, units)

      this.entryDateStr = entryDate.format(Constants.FORMATS.entryDate)
    },

    _loadExpensesData: function () {
      const self = this
      this.dataLoaded = false

      ExpenseDB.loadData(self.startDate, self.endDate)
        .then(function (docs) {
          if (self.viewStyle === Constants.VIEW_STYLE_GROUP) {
            BudgetDB.loadCategoryDataByMonth(self.startDate)
              .then(function (cats) {
                self.categoriesForMonth = cats
                self._groupExpensesData(docs)
              })
              .catch(function (err) {
                console.log(err)
                return Promise.reject(err)
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
      const self = this
      const groupedEntries = {}
      const newEntries = []

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

      const unbudgtedEntries = []
      const budgetCategories = Object.keys(this.categoriesForMonth)
      Object.entries(groupedEntries).forEach(([cat, catEntries]) => {
        let totalAmount = 0.0
        const budgetedAmount = this.categoriesForMonth[cat] || 0.0
        const type = budgetedAmount >= 0.0 ? Constants.TYPE_INCOME : Constants.TYPE_EXPENSE

        let icon = 'mdi-coin'
        if (catEntries.length > 0) {
          icon = catEntries[0].icon
          catEntries.forEach(function (entry) {
            totalAmount += entry.amount
          })
        }

        const newEntry = { type: type, icon: icon, category: cat, amount: totalAmount, budgetedAmount: budgetedAmount }

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
      const self = this

      // Load Categories (includes icons)
      BudgetDB.getCategories(BudgetDB.QUERIES.ACTIVE_AFTER(Moment(this.startDate)))
        .then(function (cats) {
          // Mapping from Category name to Icon
          self.iconMap = cats

          // Set Category List from budget entries
          self.categories = Object.keys(cats)
        })
        .then(function () {
          // Load Categories used for the current month
          // The point being to get a list of the categories used for Unbudgeted
          // entries and make them available for re-use.
          ExpenseDB.loadCategories(self.startDate, self.endDate)
            .then(function (cats) {
              const catNames = cats.map(obj => obj.category)
              const allCats = self.categories.concat(catNames).sort()

              // Filter out dups
              self.categories = [...new Set(allCats)]
            })
        })
        .catch(function (err) {
          self.displayAlert('mdi-alert-octagon', 'red', err, 60)
        })
    },

    removeTag: function (tag) {
      const index = this.entry.tags.indexOf(tag)
      this.entry.tags.splice(index, 1)
    },

    viewStyleChange: function () {
      if (this.searchText) {
        this.search()
      } else {
        this.refreshData()
      }
    },

    changeMonth: function () {
      this.startDate = Moment(this.monthToView, 'YYYY-MM', true).startOf('month').toDate()
      this.endDate = Moment(this.monthToView, 'YYYY-MM', true).endOf('month').toDate()
      this.currentMonthName = Format.monthNumberToName(this.startDate.getMonth())

      this.$route.params.category = null
      this.viewingAll = false

      this._loadCategoryData()

      this.refreshData()
    },

    // This is called from ExpenseCategory when the user clicks on the grouped
    // expense category name
    viewEntriesInGroup: function (category) {
      this.searchText = category
      this.viewStyle = Constants.VIEW_STYLE_LIST
      // this.search()
    },

    recalculateRollover: function () {
      const self = this
      const viewDate = new Moment(this.startDate)

      ExpenseDB.ensureRollover(viewDate.month(), false)
        .then(() => {
          // console.log(`MTV [${self.monthToView}] | VD [${viewDate.format('YYYY-MM')}]`)
          // self.monthToView = viewDate.format('YYYY-MM')
          self._loadCategoryData()
          self.refreshData()
        })
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
      viewingAll: false,
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
        },
        recalculateRollover: {
          labels: ['Recalculate Montly Rollover'],
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
        tags: []
      },
      showDateMenu: false,
      showAddEditSheet: false,
      showOverbudget: false,
      tagList: [],
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
