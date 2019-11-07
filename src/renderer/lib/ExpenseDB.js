import Datastore from 'nedb'
import Constants from './Constants'
import Moment from 'moment'

const { app } = require('electron').remote

const dbFileName = (process.env.NODE_ENV === 'development') ? 'expenses-dev.sxp' : 'expenses.sxp'
var _DB = new Datastore({
  filename: app.getPath('documents') + '/Sixpence/' + dbFileName,
  autoload: true,
  timestampData: true
})
// -----------------------------------------------------------------------------
export default {

  compact: function (cb) {
    _DB.persistence.compactDatafile()
    _DB.once('compaction.done', (event) => {
      cb()
    })
  },

  loadData: function (startDate, endDate) {
    var query = {}
    if (startDate && endDate) {
      query = { $where: function () { return this.date >= startDate && this.date <= endDate } }
    }

    var promise = new Promise(function (resolve, reject) {
      _DB.find(query)
        .sort({ date: 1, type: 1, category: 1, amount: -1 })
        .exec(function (err, docs) {
          if (err) {
            reject(err)
          } else {
            resolve(docs)
          }
        })
    })

    return promise
  },

  loadCategories: function (startDate, endDate) {
    var query = { $where: function () { return this.date >= startDate && this.date <= endDate } }

    var promise = new Promise(function (resolve, reject) {
      _DB.find(query, { _id: 0, category: 1 }).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          resolve(docs)
        }
      })
    })

    return promise
  },

  search: function (startDate, endDate, searchTerms, sort = { type: 1, date: 1, category: 1, amount: -1 }) {
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

    var promise = new Promise(function (resolve, reject) {
      _DB.find(query).sort(sort).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          resolve(docs)
        }
      })
    })

    return promise
  },

  // monthNumber - 0-based
  _createRolloverEntry: function (monthNumber) {
    var self = this

    var currMonth = Moment().month(monthNumber)
    var prevMonth = Moment().month(monthNumber).subtract(1, 'month')

    var currMonthStart = currMonth.startOf('month').toDate()
    var prevMonthStart = prevMonth.startOf('month').toDate()
    var prevMonthEnd = prevMonth.endOf('month').toDate()

    var promise = this.loadData(prevMonthStart, prevMonthEnd)
      .then(function (docs) {
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
        //  - Income, Category: Constants.ROLLOVER_CATEGORY, amount: income + expense
        var savePromise = self.save(
          {
            type: Constants.TYPE_INCOME,
            date: currMonthStart,
            icon: 'mdi-transfer',
            category: Constants.ROLLOVER_CATEGORY,
            amount: income + expense,
            notes: 'Balance Rolled Over from Previous Month'
          }
        )

        return savePromise
      })
      .catch(function (err) {
        return Promise.reject(err)
      })

    return promise
  },

  // monthNumber - 0-based
  ensureRollover: function (monthNumber) {
    var self = this

    var currMonthStart = Moment().month(monthNumber).startOf('month').toDate()
    var currMonthEnd = Moment().month(monthNumber).endOf('month').toDate()

    var promise = this.search(currMonthStart, currMonthEnd, { 'category': Constants.ROLLOVER_CATEGORY })
      .then(function (docs) {
        if (docs.length === 0) {
          return self._createRolloverEntry(monthNumber)
        } else {
          return Promise.resolve(true)
        }
      })
      .catch(function (err) {
        return Promise.reject(err)
      })

    return promise
  },

  delete: function (id) {
    var promise = new Promise(function (resolve, reject) {
      _DB.remove({ _id: id }, {}, function (err, count) {
        if (err) {
          reject(err)
        } else {
          resolve(count)
        }
      })
    })

    return promise
  },

  save: function (entry) {
    var promise = new Promise(function (resolve, reject) {
      _DB.update({ _id: entry._id }, entry, { upsert: true }, function (err, numReplaced, upsert) {
        if (err) {
          reject(err)
        } else {
          resolve(numReplaced, upsert)
        }
      })
    })

    return promise
  }

}
