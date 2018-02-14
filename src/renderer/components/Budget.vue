<template>
  <div>
    <v-toolbar color="deep-purple accent-2" dark>
      <v-toolbar-title>Budget</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-chip label color="green accent-1" text-color="black">
          <v-icon left>mdi-currency-usd</v-icon>
          <span class="subheading">{{ formatMoney(totalIncome) }}</span>
        </v-chip>
        <v-chip label color="red accent-1" text-color="black">
          <v-icon left>mdi-currency-usd-off</v-icon>
          <span class="subheading">{{ formatMoney(totalExpenses) }}</span>
        </v-chip>
        <v-chip label color="green" text-color="black">
          <v-icon left>mdi-cash-multiple</v-icon>
          <span class="subheading">{{ formatMoney(totalIncome + totalExpenses) }}</span>
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
            :items="iconList"
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
        <v-text-field
          name="category"
          label="Category"
          id="category"
          v-model="entry.category">
        </v-text-field>
        <v-text-field
          name="amount"
          label="Amount"
          id="amount"
          v-model="entry.amount">
        </v-text-field>
        <v-text-field
          name="notes"
          label="Notes"
          id="notes"
          v-model="entry.notes">
        </v-text-field>
        <v-btn color="primary" @click="saveRecord()">Save</v-btn>
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
import BudgetEntry from './BudgetEntry'
import Datastore from 'nedb'
import Icons from '../lib/icons'

const {app} = require('electron').remote

export default {
  name: 'Budget',
  components: { BudgetEntry },

  mounted () {
    this.db = new Datastore({
      filename: this.dbPath,
      autoload: true,
      timestampData: true
    })
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
    formatMoney: function (amount) {
      return (amount.toLocaleString('en-US', {style: 'currency', currency: 'USD'}))
    }
    // saveEntry: function () {
    //   var doc = {
    //     icon: 'cash-usd',
    //     category: 'Income:Salary',
    //     amount: 4899.42,
    //     first_due: 1,
    //     frequency: 1,
    //     notes: 'Cengage Learning, Inc'
    //   }
    //
    //   this.db.insert(doc, function (err, newDoc) {
    //     if (err) {
    //       // TODO: Better error handling, flash or dialog or ?????
    //       console.log(err)
    //     } else {
    //       console.log(newDoc)
    //     }
    //   })
    // }
  },

  data () {
    return {
      dbPath: app.getPath('documents') + '/Sixpence/budget.spx',
      db: null,
      iconList: Icons,
      budget: [
        {
          _id: '000000',
          icon: 'cash-usd',
          category: 'Income:Salary',
          amount: 2500.00,
          first_due: 1,
          frequency: 1,
          notes: 'Jobs R US'
        },
        {
          _id: '000001',
          icon: 'cash-usd',
          category: 'Income:Spouse Salary',
          amount: 1600.00,
          first_due: 1,
          frequency: 1,
          notes: 'Acme Hole Factory'
        },
        {
          _id: '000002',
          icon: 'fuel',
          category: 'Personal:Gas',
          amount: -120.00,
          first_due: 1,
          frequency: 1,
          notes: ''
        },
        {
          _id: '000003',
          icon: 'towing',
          category: 'Personal:AAA',
          amount: -149.00,
          first_due: 1,
          frequency: 12,
          notes: 'Cate, Craig & Nate'
        },
        {
          _id: '000004',
          icon: 'car',
          category: 'Auto:Registration',
          amount: -60.00,
          first_due: 2,
          frequency: 12,
          notes: 'Yaris & G6'
        },
        {
          _id: '000005',
          icon: 'account',
          category: 'Bills:Life Insurance',
          amount: -200.00,
          first_due: 2,
          frequency: 3,
          notes: 'Craig & Cate'
        }
      ],
      entry: {
        _id: null,
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
