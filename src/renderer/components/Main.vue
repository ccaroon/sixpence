<template>
  <div>
    <v-responsive class="green lighten-1">
      <v-container fill-height>
        <v-layout align-center row>
          <v-flex xs1>
            <img src="../assets/logo.png" />
          </v-flex>
          <v-flex text-xs-center>
            <h3 id="main-app-name" class="display-3">Sixpence</h3>A Simple Budget Manager
          </v-flex>
        </v-layout>
      </v-container>
    </v-responsive>
    <v-container>
      <v-layout align-center row>
        <v-flex text-xs-center>
          <v-btn id="main-budget-button" large color="green" @click="$router.push(`/budget`)">
            <v-icon>mdi-format-list-checks</v-icon>&nbsp;&nbsp;Budget
          </v-btn>
          <v-btn id="main-expense-button" large color="red" @click="$router.push(`/expenses`)">
            <v-icon>mdi-currency-usd</v-icon>Expenses
          </v-btn>
          <v-btn
            id="main-report-button"
            large
            color="orange lighten-2"
            @click="$router.push(`/report/list`)"
          >
            <v-icon>mdi-file-chart</v-icon>Reports
          </v-btn>
        </v-flex>
      </v-layout>
    </v-container>
    <v-divider></v-divider>
    <template v-if="notifications.length > 0">
      <v-alert
        v-for="(note, index) in notifications"
        :key="index"
        :icon="note.icon"
        :value="true"
        :type="note.type"
      >
        {{ note.message }}
        <v-btn
          v-if="note.handler"
          dark
          round
          absolute
          right
          @click="note.handler.action(note.handler.params)"
        >Update</v-btn>
      </v-alert>
    </template>
    <template v-else>
      <v-alert outline color="grey" icon="mdi-note" value="true">No Notifications</v-alert>
    </template>
  </div>
</template>

<script>
import DBMigrations from '../lib/DBMigrations'

export default {
  name: 'Main',

  mounted () {
    this.checkForDBMigrations()
  },

  methods: {
    checkForDBMigrations: function () {
      var budgetChecks = DBMigrations.checkBudgetDb()

      budgetChecks.forEach(check => {
        check.needsApplying
          .then(needed => {
            if (needed) {
              var type = check.migration.critical ? 'error' : 'info'
              this.addNotification(
                'mdi-update',
                type,
                `Database Update: ${check.migration.name} - ${check.migration.desc}`,
                {action: this.applyMigration, params: check.migration}
              )
            }
          })
          .catch(err => {
            this.addNotification('mdi-alert-octagram', 'error', `Database Update Check Failed: ${err}`)
          })
      })

      // var expenseChecks = DBMigrations.checkExpenseDb()
    },

    applyMigration: function (mig) {
      mig.apply()
        .then(num => {
          this.notifications = []
          this.addNotification('mdi-update', 'success', `${mig.name} successfully applied. ${num} entries updated.`)
        })
        .catch(err => {
          this.notifications = []
          this.addNotification('mdi-alert-octagram', 'error', `${mig.name} failed: ${err}`)
        })
    },

    addNotification: function (icon, type, msg, action = null) {
      this.notifications.push({icon: icon, type: type, message: msg, handler: action})
    }
  },

  data () {
    return {
      notifications: []
    }
  }
}
</script>
