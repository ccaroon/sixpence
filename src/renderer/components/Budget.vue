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
        <v-chip label :color="totalIncome + totalExpenses >= 0 ? 'green' : 'red'" text-color="black">
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

    <v-divider></v-divider>
    <v-subheader>Add Entry</v-subheader>

    <v-container fluid>
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
              v-model="entry.category">
            </v-text-field>
        </v-flex>
        <v-flex xs1>
            <v-text-field
              name="amount"
              label="Amount"
              id="amount"
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
            <v-btn color="primary" @click="saveEntry()">Save</v-btn>
        </v-flex>
      </v-layout>
    </v-container>


    <!-- <v-btn
      color="green"
      dark
      fab>
      <v-icon>mdi-plus-box</v-icon>
    </v-btn> -->

  </div>
</template>

<script>
// TODO: Add Entry Form Validation

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
      var income = 0
      for (var i = 0; i < this.budget.length; i++) {
        var entry = this.budget[i]
        if (entry.amount >= 0) {
          income += entry.amount
        }
      }
      return (income)
    },

    totalExpenses: function () {
      var expense = 0
      for (var i = 0; i < this.budget.length; i++) {
        var entry = this.budget[i]
        if (entry.amount < 0) {
          expense += (entry.amount / entry.frequency)
        }
      }
      return (expense)
    }
  },

  methods: {
    _loadBudgetData: function () {
      var self = this
      this.db.find({}, function (err, docs) {
        if (err) {
          // TODO: handle errors
          console.log(err)
        } else {
          self.budget = docs
        }
      })
    },

    _clearEntry: function () {
      this.entry = {}
    },

    saveEntry: function () {
      var self = this
      this.entry.amount = parseFloat(this.entry.amount)

      this.db.insert(this.entry, function (err, newDoc) {
        if (err) {
          // TODO: Better error handling, flash or dialog or ?????
          console.log(err)
        } else {
          self.budget.push(newDoc)
          // console.log(newDoc)
        }
      })

      this._clearEntry()
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
        // _id: null,
        icon: null,
        category: null,
        amount: null,
        first_due: null,
        frequency: null,
        notes: null
      }
    }
  }
}
</script>
