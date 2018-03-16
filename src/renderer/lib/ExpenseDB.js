import Datastore from 'nedb'

const {app} = require('electron').remote

export default {

  db: new Datastore({
    filename: app.getPath('documents') + '/Sixpence/expenses.sxp',
    autoload: true,
    timestampData: true
  }),

  loadData: function (startDate, endDate, cb) {
    var query = {}
    if (startDate && endDate) {
      query = { $where: function () { return this.date >= startDate && this.date <= endDate } }
    }

    this.db.find(query).sort({type: 1, category: 1, date: 1, amount: -1}).exec(cb)
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
  }

}
