import Datastore from 'nedb'

const {app} = require('electron').remote

export default {

  db: new Datastore({
    filename: app.getPath('documents') + '/Sixpence/expenses.sxp',
    autoload: true,
    timestampData: true
  }),

  loadData: function (cb) {
    this.db.find({}).sort({type: 1, date: 1, category: 1, amount: -1}).exec(cb)
  },

  search: function (searchTerms, sort, cb) {
    if (!sort) {
      sort = {type: 1, date: 1, category: 1, amount: -1}
    }

    this.db.find(searchTerms).sort(sort).exec(cb)
  },

  delete: function (id, cb) {
    this.db.remove({ _id: id }, {}, cb)
  },

  save: function (entry, cb) {
    this.db.update({_id: entry._id}, entry, { upsert: true }, cb)
  },

  writeExampleEntry: function () {
    var entry = {
      type: 1,
      date: new Date(),
      category: 'Bills:Electricity',
      amount: -78.34,
      notes: ''
    }
    this.save(entry, function (err, doc) {
      if (err) {
        console.log(err)
      }
    })
  }

}
