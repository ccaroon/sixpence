<template>
  <div>
    <v-toolbar color="grey darken-2" dark dense app fixed>
      <v-toolbar-title>Budget</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-flex>
        <v-btn-toggle v-model="freqFilter" dark class="orange lighten-2">
          <v-btn flat>
            <v-icon>mdi-numeric-1-box</v-icon>
          </v-btn>
          <v-btn flat>
            <v-icon>mdi-numeric-2-box</v-icon>
          </v-btn>
          <v-btn flat>
            <v-icon>mdi-numeric-3-box</v-icon>
          </v-btn>
          <v-btn flat>
            <v-icon>mdi-numeric-6-box</v-icon>
          </v-btn>
          <v-btn flat>
            <v-icon>fa-calendar</v-icon>
          </v-btn>
          <v-btn flat>
            <v-icon>mdi-all-inclusive</v-icon>
          </v-btn>
        </v-btn-toggle>
      </v-flex>
      <v-flex>
        <v-toolbar-items>
          <v-chip color="green accent-1" text-color="black" tabindex="-1" disabled>
            <v-icon left>mdi-currency-usd</v-icon>
            <span class="subheading">{{ utils.formatMoney(totalIncome) }}</span>
          </v-chip>
          <v-chip color="red accent-1" text-color="black" tabindex="-1" disabled>
            <v-icon left>mdi-currency-usd-off</v-icon>
            <span class="subheading">{{ utils.formatMoney(totalExpenses) }}</span>
          </v-chip>
          <v-chip :color="totalIncome + totalExpenses >= 0 ? 'green accent-3' : 'red accent-3'" text-color="black" tabindex="-1" disabled>
            <v-icon left>mdi-cash-multiple</v-icon>
            <span class="subheading">{{ utils.formatMoney(totalIncome + totalExpenses) }}</span>
          </v-chip>
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

    <v-list dense v-for="entry in budget"
      v-bind:key="entry._id">
      <BudgetEntry
        v-bind:entry="entry"
        v-on:editEntry="editEntry"
        v-on:refreshData="refreshData"
        v-on:displayAlert="displayAlert">
      </BudgetEntry>
    </v-list>

    <div class="text-xs-center">
      <v-bottom-sheet v-model="showAddEditSheet">
        <v-btn
          slot="activator"
          color="green accent-3"
          @click="entry = {}"
          fixed bottom right dark fab>
          <v-icon>mdi-plus</v-icon>
        </v-btn>
        <v-card>
          <v-form ref="budgetForm">
            <v-layout row>
              <v-flex xs1>
                <v-select
                  ref="iconSelect"
                  :items="formData.icons"
                  v-model="entry.icon"
                  label="Icon"
                  single-line
                  dense
                  tabindex="1"
                  hint="Choose an Icon"
                  append-icon="mdi-menu-down">
                  <template slot="selection" slot-scope="data">
                    <v-icon>{{ data.item.value }}</v-icon>
                  </template>
                  <template slot="item" slot-scope="data">
                    <v-icon>{{ data.item.value }}</v-icon>
                  </template>
                </v-select>
              </v-flex>
              <v-flex xs2>
                <v-select
                  :items="formData.categories"
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
              <v-flex xs2>
                <v-select
                  :items="formData.frequency"
                  v-model="entry.frequency"
                  label="Frequency"
                  single-line
                  dense
                  required
                  tabindex="4"
                  :rules="rules.frequency"
                  autocomplete
                  hint="How Frequently Does This Item Occur?"
                  append-icon="mdi-menu-down">
                </v-select>
              </v-flex>
              <v-flex xs2>
                <v-select
                  :items="formData.months"
                  v-model="entry.first_due"
                  label="First Due"
                  single-line
                  dense
                  required
                  tabindex="5"
                  :rules="rules.first_due"
                  autocomplete
                  hint="In What Month Is This Item First Due?"
                  append-icon="mdi-menu-down">
                </v-select>
              </v-flex>
              <v-flex xs3>
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
import BudgetEntry from './BudgetEntry'
import BudgetDB from '../lib/BudgetDB'
import StaticData from '../lib/static_data'
import Utils from '../lib/utils'

const BUDGET_TYPE_INCOME = 0
const BUDGET_TYPE_EXPENSE = 1
// const {app} = require('electron').remote

export default {
  name: 'Budget',
  components: { BudgetEntry },

  mounted () {
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
    refreshData: function () {
      this._loadBudgetData()
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

        BudgetDB.search(query, null, function (err, docs) {
          if (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err)
          } else {
            self.budget = docs
          }
        })
      }
    },

    clearSearch: function () {
      if (this.searchText) {
        this.searchText = null
        this.freqFilter = 5
        this.refreshData()
      }
    },

    filterByFreq: function () {
      var self = this

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
        BudgetDB.search({frequency: freq}, null, function (err, docs) {
          if (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err)
          } else {
            self.budget = docs
          }
        })
      } else {
        this.refreshData()
      }
    },

    _loadBudgetData: function () {
      var self = this

      BudgetDB.loadData(function (err, docs) {
        if (err) {
          self.displayAlert('mdi-alert-octagon', 'red', err)
        } else {
          self.budget = docs
          self._loadCategoryData()
        }
      })
    },

    _loadCategoryData: function () {
      var allCats = this.budget.map(function (entry) {
        return (entry.category)
      })

      var uniqueCats = Array.from(new Set(allCats))

      // var catsForSelect = uniqueCats.map(function (category) {
      //   return ({text: category, value: '*' + category + '*'})
      // })
      // console.log(catsForSelect)

      // Set Category List from budget entries
      this.formData.categories = this.formData.categories.concat(this.formData.categories, uniqueCats)
    },

    _clearEntry: function () {
      this.entry = {}
    },

    displayAlert: function (icon, color, message) {
      this.alert.icon = icon
      this.alert.color = color
      this.alert.message = message
      this.alert.visible = true
    },

    editEntry: function (entry) {
      this.entry = entry
      this.showAddEditSheet = true
    },

    saveEntry: function () {
      var self = this

      if (this.$refs.budgetForm.validate()) {
        this.entry.icon = this.entry.icon ? this.entry.icon : StaticData.icons[0].value
        this.entry.amount = parseFloat(this.entry.amount)
        this.entry.type = this.entry.amount > 0 ? BUDGET_TYPE_INCOME : BUDGET_TYPE_EXPENSE

        BudgetDB.save(this.entry, function (err, numReplaced, upsert) {
          if (err) {
            self.displayAlert('mdi-alert-octagon', 'red', err)
          } else {
            self._loadBudgetData()
            self._clearEntry()
            self.$refs.iconSelect.$el.focus()

            self.displayAlert('mdi-content-save', 'green', 'Entry Successfully Saved')
          }
        })
      }
    }
  },

  watch: {
    freqFilter: 'filterByFreq'
  },

  data () {
    return {
      formData: StaticData,
      utils: Utils,
      searchText: null,
      freqFilter: 5,
      budget: [],
      alert: {
        visible: false,
        icon: 'mdi-alert',
        color: 'green',
        message: ''
      },
      entry: {
        type: null,
        icon: null,
        category: null,
        amount: null,
        first_due: null,
        frequency: null,
        notes: null
      },
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
        first_due: [
          fdue => !!fdue || 'First Due Month is required'
        ]
      }
    }
  }
}
</script>
