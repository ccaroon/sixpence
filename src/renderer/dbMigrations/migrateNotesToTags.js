import ExpenseDB from '../lib/ExpenseDB'
// -----------------------------------------------------------------------------
export default {
  name: 'migrateNotesToTags',
  desc: 'Migrate the Notes field to Tags.',
  note: 'Automatic Migration not implemented! Manually edit an entry to add tags and remove notes.',

  critical: false,
  active: true,

  check: function () {
    return ExpenseDB.count({ notes: { $exists: true } })
      .then(num => {
        return (num > 0)
      })
  },

  apply: function () {
    return Promise.resolve(null)
  }
}
