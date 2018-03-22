import Datastore from 'nedb'

const {app} = require('electron').remote

var _DB = new Datastore({
  filename: app.getPath('documents') + '/Sixpence/expenses.sxp',
  autoload: true,
  timestampData: true
})
// -----------------------------------------------------------------------------
export default {

  loadData: function (startDate, endDate, cb) {
    var query = {}
    if (startDate && endDate) {
      query = { $where: function () { return this.date >= startDate && this.date <= endDate } }
    }

    _DB.find(query).sort({type: 1, category: 1, date: 1, amount: -1}).exec(cb)
  },

  search: function (searchTerms, sort, cb) {
    if (!sort) {
      sort = {type: 1, date: 1, category: 1, amount: -1}
    }

    _DB.find(searchTerms).sort(sort).exec(cb)
  },

  delete: function (id, cb) {
    _DB.remove({ _id: id }, {}, cb)
  },

  save: function (entry, cb) {
    _DB.update({_id: entry._id}, entry, { upsert: true }, cb)
  }

}
