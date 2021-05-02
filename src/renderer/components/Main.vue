<template>
  <div>
    <v-responsive class="green lighten-1">
      <v-container fill-height>
        <v-row align="center">
          <v-col cols="auto">
            <img src="../assets/logo.png" />
          </v-col>
          <v-col cols="auto">
            <p class="display-4">Sixpence</p>
            <p class="subtitle-1">A Simple Budget Manager</p>
          </v-col>
        </v-row>
      </v-container>
    </v-responsive>
    <v-container>
      <v-row align="center" justify="space-around" class="pa-1">
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
      </v-row>
      <v-row align="center" justify="space-around" class="pa-1">
        <v-btn id="main-settings-button" large color="grey" @click="$router.push(`/settings`)">
          <v-icon>mdi-settings</v-icon>Settings
        </v-btn>
      </v-row>
    </v-container>
    <v-divider></v-divider>
    <template v-if="notifications.length > 0">
      <v-alert
        v-for="(note, index) in notifications"
        :key="index"
        :icon="note.icon"
        :type="note.type"
      >
        {{ note.message }}
        <v-btn
          v-if="note.handler"
          dark
          rounded
          absolute
          right
          @click="note.handler.action(note.handler.params)"
        >Update</v-btn>
      </v-alert>
    </template>
    <template v-else>
      <v-alert outlined color="grey" icon="mdi-note">No Notifications</v-alert>
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
    applyDBMigrations: function (check) {
      check.needsApplying
        .then(needed => {
          if (needed) {
            const type = check.migration.critical ? 'error' : 'info'
            this.addNotification(
              'mdi-update',
              type,
              `Database Update: ${check.migration.name} - ${check.migration.desc}`,
              { action: this.applyMigration, params: check.migration }
            )
          }
        })
        .catch(err => {
          this.addNotification('mdi-alert-octagram', 'error', `Database Update Check Failed: ${err}`)
        })
    },

    checkForDBMigrations: function () {
      const budgetChecks = DBMigrations.checkBudgetDb()
      budgetChecks.forEach(this.applyDBMigrations)

      const expenseChecks = DBMigrations.checkExpenseDb()
      expenseChecks.forEach(this.applyDBMigrations)
    },

    applyMigration: function (mig) {
      mig.apply()
        .then(num => {
          this.notifications = []
          if (num === null) {
            this.addNotification('mdi-alert', 'warning', `${mig.name}: ${mig.note}`)
          } else {
            this.addNotification('mdi-update', 'success', `${mig.name} successfully applied. ${num} entries updated.`)
          }
        })
        .catch(err => {
          this.notifications = []
          this.addNotification('mdi-alert-octagram', 'error', `${mig.name} failed: ${err}`)
        })
    },

    addNotification: function (icon, type, msg, action = null) {
      this.notifications.push({ icon: icon, type: type, message: msg, handler: action })
    }
  },

  data () {
    return {
      notifications: []
    }
  }
}
</script>
