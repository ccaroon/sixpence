import BudgetDB from '../lib/BudgetDB'
// -----------------------------------------------------------------------------
export default {
  name: 'addIsArchived',
  desc: 'Adds a new field to the database named `isArchived`. Used when marking a Budget Entry as Archived.',

  critical: true,
  active: false,

  notes: [
    'No longer necessary. Short lived for v1.9.0 only.',
    'Superseded by `addArchivedAt`.'
  ],

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
