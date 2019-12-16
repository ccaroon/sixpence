import addIsArchived from '../dbMigrations/addIsArchived'
import delIsArchived from '../dbMigrations/delIsArchived'
import addArchivedAt from '../dbMigrations/addArchivedAt'
import migrateNotesToTags from '../dbMigrations/migrateNotesToTags'
// -----------------------------------------------------------------------------
var migrations = {
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

  checkBudgetDb: function () {
    var neededMigrations = []
    migrations.budgetDB.forEach(mig => {
      if (mig.active) {
        neededMigrations.push({ migration: mig, needsApplying: mig.check() })
      }
    })

    return (neededMigrations)
  },

  checkExpenseDb: function () {
    var neededMigrations = []
    migrations.expenseDB.forEach(mig => {
      if (mig.active) {
        neededMigrations.push({ migration: mig, needsApplying: mig.check() })
      }
    })

    return (neededMigrations)
  }
}
