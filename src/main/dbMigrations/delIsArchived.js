import BudgetDB from '../lib/BudgetDB'
// -----------------------------------------------------------------------------
export default {
  name: 'delIsArchived',
  desc: 'Delete the `isArchived` flag field.',

  critical: true,
  active: true,

  actions: {
    check: async function () {
      const count = await BudgetDB.count({ isArchived: { $exists: true } })
      return count
    },

    apply: function () {
      return BudgetDB.bulkUpdate({ isArchived: { $exists: true } }, { $unset: { isArchived: true } })
    }
  }
}
