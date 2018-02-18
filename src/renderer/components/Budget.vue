<template>
  <div>
    <v-toolbar color="deep-purple accent-2" dark>
      <v-toolbar-title>Budget</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-chip label color="green accent-1" text-color="black">
          <v-icon left>mdi-currency-usd</v-icon>
          <span class="subheading">{{ utils.formatMoney(totalIncome) }}</span>
        </v-chip>
        <v-chip label color="red accent-1" text-color="black">
          <v-icon left>mdi-currency-usd-off</v-icon>
          <span class="subheading">{{ utils.formatMoney(totalExpenses) }}</span>
        </v-chip>
        <v-chip label :color="totalIncome + totalExpenses >= 0 ? 'green accent-3' : 'red accent-3'" text-color="black">
          <v-icon left>mdi-cash-multiple</v-icon>
          <span class="subheading">{{ utils.formatMoney(totalIncome + totalExpenses) }}</span>
        </v-chip>
      </v-toolbar-items>
    </v-toolbar>

    <v-list dense v-for="entry in budget"
      v-bind:key="entry._id">
      <BudgetEntry
        v-bind:entry="entry">
      </BudgetEntry>
    </v-list>

    <div class="text-xs-center">
      <v-bottom-sheet>
        <v-btn slot="activator" color="green accent-3" dark fab><v-icon>mdi-plus</v-icon></v-btn>
        <v-card>
          <v-form ref="budgetForm">
            <v-layout row>
              <v-flex xs1>
                <v-select
                  :items="formData.icons"
                  v-model="entry.icon"
                  label="Icon"
                  single-line
                  dense
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
                <v-text-field
                  name="category"
                  label="Category"
                  id="category"
                  required
                  :rules="rules.category"
                  v-model="entry.category">
                </v-text-field>
              </v-flex>
              <v-flex xs1>
                <v-text-field
                  name="amount"
                  label="Amount"
                  id="amount"
                  required
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
                  :rules="rules.frequency"
                  autocomplete
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
                  :rules="rules.first_due"
                  autocomplete
                  append-icon="mdi-menu-down">
                </v-select>
              </v-flex>
              <v-flex xs3>
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
import BudgetEntry from './BudgetEntry'
import Datastore from 'nedb'
import StaticData from '../lib/static_data'
import Utils from '../lib/utils'

const {app} = require('electron').remote

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
    _loadExpenseData: function () {
      var self = this
      this.db.find({amount: {$lt: 0}}).sort({category: 1, amount: -1}).exec(function (err, docs) {
        if (err) {
          // TODO: handle errors
          console.log(err)
        } else {
          self.budget = self.budget.concat(docs)
        }
      })
    },
    _loadBudgetData: function () {
      var self = this
      // Load Income Data First...
      this.db.find({amount: {$gt: 0}}).sort({category: 1, amount: -1}).exec(function (err, docs) {
        if (err) {
          // TODO: handle errors
          console.log(err)
        } else {
          self.budget = docs
          // ...then Load Expense Data
          self._loadExpenseData()
        }
      })
    },

    _clearEntry: function () {
      this.entry = {}
    },

    saveEntry: function () {
      var self = this

      if (this.$refs.budgetForm.validate()) {
        this.entry.icon = this.entry.icon ? this.entry.icon : StaticData.icons[0].value
        this.entry.amount = parseFloat(this.entry.amount)

        this.db.insert(this.entry, function (err, newDoc) {
          if (err) {
            // TODO: Better error handling, flash or dialog or ?????
            console.log(err)
          } else {
            self._loadBudgetData()
          }
        })

        this._clearEntry()
      }
    }
  },

  data () {
    return {
      db: new Datastore({
        filename: app.getPath('documents') + '/Sixpence/budget.spx',
        autoload: true,
        timestampData: true
      }),
      formData: StaticData,
      utils: Utils,
      budget: [],
      entry: {
        icon: null,
        category: null,
        amount: null,
        first_due: null,
        frequency: null,
        notes: null
      },
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
