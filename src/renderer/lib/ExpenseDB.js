import Datastore from 'nedb'
import Constants from './Constants'
import Moment from 'moment'

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

  loadCategories: function (startDate, endDate, cb) {
    var query = { $where: function () { return this.date >= startDate && this.date <= endDate } }

    _DB.find(query, {_id: 0, category: 1}).exec(cb)
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

  // monthNumber - 0-based
  _createRolloverEntry: function (monthNumber, resolve, reject) {
    var self = this

    var currMonth = Moment().month(monthNumber)
    var prevMonth = Moment().month(monthNumber).subtract(1, 'month')

    var currMonthStart = currMonth.startOf('month').toDate()
    var prevMonthStart = prevMonth.startOf('month').toDate()
    var prevMonthEnd = prevMonth.endOf('month').toDate()

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

  // monthNumber - 0-based
  ensureRollover: function (monthNumber) {
    var self = this

    var currMonthStart = Moment().month(monthNumber).startOf('month').toDate()
    var currMonthEnd = Moment().month(monthNumber).endOf('month').toDate()

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
