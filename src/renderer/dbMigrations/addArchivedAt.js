import BudgetDB from '../lib/BudgetDB'
// -----------------------------------------------------------------------------
export default {
  name: 'addArchivedAt',
  desc: 'Add new date field named `archivedAt`',

  critical: true,
  active: true,

  check: function () {
    return BudgetDB.count({ archivedAt: { $exists: false } })
      .then(num => {
        return (num > 0)
      })
  },

  apply: function () {
    return BudgetDB.bulkUpdate({ archivedAt: { $exists: false } }, { $set: { archivedAt: null } })
  }
}
