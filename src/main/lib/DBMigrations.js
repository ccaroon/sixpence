import addIsArchived from '../dbMigrations/addIsArchived'
import delIsArchived from '../dbMigrations/delIsArchived'
import addArchivedAt from '../dbMigrations/addArchivedAt'
import migrateNotesToTags from '../dbMigrations/migrateNotesToTags'
// -----------------------------------------------------------------------------
const migrations = {
  budgetDB: [
    addIsArchived,
    delIsArchived,
    addArchivedAt
  ],
  expenseDB: [
    migrateNotesToTags
  ]
}
// -----------------------------------------------------------------------------
export default {

  checkBudgetDb: async function () {
    const neededMigrations = []
    await migrations.budgetDB.forEach((mig) => {
      if (mig.active) {
        const needsApplying = mig.actions.check()
        neededMigrations.push({ migration: mig, needsApplying: needsApplying })

        // Have to remove 'actions' since function don't serialize via IPC
        delete mig.actions
      }
    })

    return (neededMigrations)
  },

  checkExpenseDb: function () {
    const neededMigrations = []

    migrations.expenseDB.forEach((mig) => {
      if (mig.active) {
        console.log(mig.name)
        // TODO: how to get this stupid `check` Promise to resolve
        const needsApplying = mig.actions.check()
        neededMigrations.push({ migration: mig, needsApplying: needsApplying })

        // Have to remove 'actions' since function don't serialize via IPC
        delete mig.actions
      }
    })

    return (neededMigrations)
  },

  execute: function (name) {
    // const mig = migrations[name]

    // mig.apply()
    //   .then(num => {
    //     this.notifications = []
    //     if (num === null) {
    //       this.addNotification('mdi-alert', 'warning', `${mig.name}: ${mig.note}`)
    //     } else {
    //       this.addNotification('mdi-update', 'success', `${mig.name} successfully applied. ${num} entries updated.`)
    //     }
    //   })
    //   .catch(err => {
    //     this.notifications = []
    //     this.addNotification('mdi-alert-octagram', 'error', `${mig.name} failed: ${err}`)
    //   })
  }
}
