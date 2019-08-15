import BudgetDB from '../lib/BudgetDB'
// -----------------------------------------------------------------------------
export default {
  name: 'addIsArchived',
  desc: 'Adds a new field to the database named `isArchived`. Used when marking a Budget Entry as Archived.',

  critical: true,

  check: function () {
    return BudgetDB.count({ isArchived: { $exists: false } })
      .then(num => {
        return (num > 0)
      })
  },

  apply: function () {
    return BudgetDB.bulkUpdate({ isArchived: { $exists: false } }, { $set: { isArchived: false } })
  }
}
