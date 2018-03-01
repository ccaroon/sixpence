import Datastore from 'nedb'

const {app} = require('electron').remote

export default {

  db: new Datastore({
    filename: app.getPath('documents') + '/Sixpence/budget.sxp',
    autoload: true,
    timestampData: true
  }),

  loadExpenseData: function (cb) {
    this.db.find({amount: {$lt: 0}}).sort({category: 1, amount: -1}).exec(cb)
  },

  loadIncomeData: function (cb) {
    this.db.find({amount: {$gt: 0}}).sort({category: 1, amount: -1}).exec(cb)
  },

  delete: function (id, cb) {
    this.db.remove({ _id: id }, {}, cb)
  },

  save: function (entry, cb) {
    // if (entry._id) {
    //   this.db.update(entry, db)
    // } else {
    //   this.db.update(...)
    // }
    this.db.update({_id: entry._id}, entry, { upsert: true }, cb)
  }

}
