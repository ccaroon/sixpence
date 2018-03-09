<template>
<div>
    <v-toolbar color="grey darken-2" dark dense app fixed>
      <v-toolbar-title>Expenses - {{ currentMonthName }}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-flex>
        <v-btn-toggle v-model="viewStyle" dark class="orange lighten-2">
          <v-btn flat>
            <v-icon>mdi-view-list</v-icon>
          </v-btn>
          <v-btn flat>
            <v-icon>mdi-chart-bar</v-icon>
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

    <v-list v-if="viewStyle === 0" dense v-for="entry in expenses"
      v-bind:key="entry._id">
      <ExpenseEntry
      v-bind:entry="entry"
      v-on:editEntry="editEntry"
      v-on:refreshData="refreshData"
      v-on:displayAlert="displayAlert">
      </ExpenseEntry>
    </v-list>

    <v-list v-if="viewStyle === 1" dense v-for="entry in expenses"
      v-bind:key="entry._id">
      <ExpenseProgress
        v-bind:entry="entry">
      </ExpenseProgress>
    </v-list>


  <!-- <v-menu
    ref="dateMenu"
    lazy
    :close-on-content-click="false"
    v-model="showDateMenu"
    transition="scale-transition"
    offset-y
    full-width
    :nudge-right="40"
    min-width="290px"
    :return-value.sync="entry.date">
    <v-text-field
      slot="activator"
      label="Date"
      v-model="entry.date"
      prepend-icon="mdi-calendar-range"
      readonly
    ></v-text-field>
    <v-date-picker v-model="entry.date"
      next-icon="mdi-chevron-right"
      prev-icon="mdi-chevron-left"
      color="green accent-3">
      <v-spacer></v-spacer>
      <v-btn flat color="error" @click="showDateMenu = false">Cancel</v-btn>
      <v-btn color="success" @click="$refs.dateMenu.save(entry.date)">OK</v-btn>
    </v-date-picker>
  </v-menu> -->

</div>
</template>

<script>
import ExpenseEntry from './ExpenseEntry'
import ExpenseProgress from './ExpenseProgress'
import ExpensesDB from '../lib/ExpensesDB'
import StaticData from '../lib/static_data'
import Utils from '../lib/utils'

export default {
  name: 'Expenses',
  components: { ExpenseEntry, ExpenseProgress },

  mounted () {
    this.currentMonthName = this.utils.monthNumberToName(new Date().getMonth())
    this._loadExpensesData()
    // ExpensesDB.writeExampleEntry()
  },

  computed: {
    totalIncome: function () {
      var income = 0.0
      for (var i = 0; i < this.expenses.length; i++) {
        var entry = this.expenses[i]
        if (entry.amount >= 0.0) {
          income += entry.amount
        }
      }
      return (income)
    },

    totalExpenses: function () {
      var expense = 0.0
      for (var i = 0; i < this.expenses.length; i++) {
        var entry = this.expenses[i]
        if (entry.amount < 0.0) {
          expense += entry.amount
        }
      }
      return (expense)
    }
  },

  methods: {
    search: function () {
      console.log('search')
    },

    clearSearch: function () {
      console.log('clearSearch')
    },

    editEntry: function () {
      console.log('editEntry')
    },

    refreshData: function () {
      console.log('refreshData')
    },

    displayAlert: function () {
      console.log('displayAlert')
    },

    _loadExpensesData: function () {
      var self = this

      // TODO: restrict data to current month
      ExpensesDB.loadData(function (err, docs) {
        if (err) {
          console.log(err)
        } else {
          self.expenses = docs
        }
      })
    }
  },

  data () {
    return {
      formData: StaticData,
      utils: Utils,
      viewStyle: 0,
      expenses: [],
      searchText: null,
      currentMonthName: null,
      // alert: {
      //   visible: false,
      //   icon: 'mdi-alert',
      //   color: 'green',
      //   message: ''
      // },
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
