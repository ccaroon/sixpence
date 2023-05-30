import BudgetDB from '../lib/BudgetDB'
// -----------------------------------------------------------------------------
export default {
  name: 'addArchivedAt',
  desc: 'Add new date field named `archivedAt`',

  critical: true,
  active: true,

  actions: {
    check: function () {
      return BudgetDB.count({ archivedAt: { $exists: false } })
    },

    apply: function () {
      return BudgetDB.bulkUpdate({ archivedAt: { $exists: false } }, { $set: { archivedAt: null } })
    }
  }
}
