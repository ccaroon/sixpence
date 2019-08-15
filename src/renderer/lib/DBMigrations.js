// import BudgetDB from './BudgetDB'

import addIsArchived from '../dbMigrations/addIsArchived'
// -----------------------------------------------------------------------------
var migrations = {
  budgetDB: [
    addIsArchived
  ]
}
// -----------------------------------------------------------------------------
export default {

  checkBudgetDb: function () {
    var neededMigrations = []
    migrations.budgetDB.forEach(mig => {
      neededMigrations.push({ migration: mig, needsApplying: mig.check() })
    })

    return (neededMigrations)
  },

  checkExpenseDb: function () {
    return ([])
  }
}
