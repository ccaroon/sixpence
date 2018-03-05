<template>
<div>
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
  </v-menu>
</div>
</template>

<script>
// import BudgetDB from '../lib/BudgetDB'
import StaticData from '../lib/static_data'
import Utils from '../lib/utils'

export default {
  name: 'Expenses',
  // components: { ... },

  methods: {},

  data () {
    return {
      formData: StaticData,
      utils: Utils,
      expenses: [],
      // alert: {
      //   visible: false,
      //   icon: 'mdi-alert',
      //   color: 'green',
      //   message: ''
      // },
      entry: {
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
