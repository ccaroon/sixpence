import BudgetDB from '../lib/BudgetDB'
// -----------------------------------------------------------------------------
export default {
  name: 'delIsArchived',
  desc: 'Delete the `isArchived` flag field.',

  critical: true,
  active: true,

  check: function () {
    return BudgetDB.count({ isArchived: { $exists: true } })
      .then(num => {
        return (num > 0)
      })
  },

  apply: function () {
    return BudgetDB.bulkUpdate({ isArchived: { $exists: true } }, { $unset: { isArchived: true } })
  }
}
