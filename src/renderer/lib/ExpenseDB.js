import Datastore from 'nedb'
import Constants from './Constants'

const {app} = require('electron').remote
const CAT_ROLLOVER = 'Sixpence:Rollover'

const dbFileName = (process.env.NODE_ENV === 'development') ? 'expenses-dev.sxp' : 'expenses.sxp'
var _DB = new Datastore({
  filename: app.getPath('documents') + '/Sixpence/' + dbFileName,
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

    _DB.find(query).sort({date: 1, type: 1, category: 1, amount: -1}).exec(cb)
  },

  search: function (startDate, endDate, searchTerms, sort, cb) {
    var query = searchTerms
    if (startDate && endDate) {
      query = {
        $and:
        [
          searchTerms,
          { $where: function () { return this.date >= startDate && this.date <= endDate } }
        ]
      }
    }

    if (!sort) {
      sort = {type: 1, date: 1, category: 1, amount: -1}
    }

    _DB.find(query).sort(sort).exec(cb)
  },

  // monthNumber - 1-based
  _createRolloverEntry: function (monthNumber, resolve, reject) {
    var self = this
    var now = new Date()

    var currMonthStart = new Date(now.getFullYear(), monthNumber - 1, 1)
    var prevMonthStart = new Date(now.getFullYear(), monthNumber - 2, 1)
    var prevMonthEnd = new Date(now.getFullYear(), monthNumber - 1, 0)

    this.loadData(prevMonthStart, prevMonthEnd, function (err, docs) {
      if (err) {
        reject(err)
      } else {
        var income = 0.0
        var expense = 0.0
        docs.forEach(function (entry) {
          if (entry.amount >= 0.0) {
            income += entry.amount
          } else {
            expense += entry.amount
          }
        })

        // insert record for first day of monthNumber
        //  - Income, Category: CAT_ROLLOVER, amount: income + expense
        self.save({
          type: Constants.TYPE_INCOME,
          date: currMonthStart,
          icon: 'mdi-transfer',
          category: CAT_ROLLOVER,
          amount: income + expense,
          notes: 'Balance Rolled Over from Previous Month'
        }, function (err, num, upsert) {
          if (err) {
            reject(err)
          } else {
            resolve()
          }
        })
      }
    })
  },

  // monthNumber - 1-based
  ensureRollover: function (monthNumber) {
    var self = this
    var now = new Date()
    var currMonthStart = new Date(now.getFullYear(), monthNumber - 1, 1)
    var currMonthEnd = new Date(now.getFullYear(), monthNumber, 0)

    var promise = new Promise(function (resolve, reject) {
      self.search(currMonthStart, currMonthEnd, {'category': CAT_ROLLOVER}, null, function (err, docs) {
        if (err) {
          reject(err)
        } else {
          if (docs.length === 0) {
            // TODO: Use another promise here instead of passing along resolve & reject???
            self._createRolloverEntry(monthNumber, resolve, reject)
          } else {
            resolve()
          }
        }
      })
    })

    return (promise)
  },

  delete: function (id, cb) {
    _DB.remove({ _id: id }, {}, cb)
  },

  save: function (entry, cb) {
    _DB.update({_id: entry._id}, entry, { upsert: true }, cb)
  }

}
