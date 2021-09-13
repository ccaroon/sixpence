import Datastore from 'nedb'
import Constants from './Constants'
import Moment from 'moment'

const { app } = require('electron').remote

const dbFileName = (process.env.NODE_ENV === 'development') ? 'expenses-dev.sxp' : 'expenses.sxp'
const _DB = new Datastore({
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
    let query = {}
    if (startDate && endDate) {
      query = { $where: function () { return this.date >= startDate && this.date <= endDate } }
    }

    const promise = new Promise(function (resolve, reject) {
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
    const query = { $where: function () { return this.date >= startDate && this.date <= endDate } }

    const promise = new Promise(function (resolve, reject) {
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

  search: function (startDate, endDate, searchTerms, sort = { type: 1, date: 1, category: 1, amount: -1 }, fields = {}) {
    let query = searchTerms
    if (startDate && endDate) {
      query = {
        $and:
          [
            searchTerms,
            { $where: function () { return this.date >= startDate && this.date <= endDate } }
          ]
      }
    }

    const promise = new Promise(function (resolve, reject) {
      _DB.find(query, fields).sort(sort).exec(function (err, docs) {
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
    const self = this

    const currMonth = Moment().month(monthNumber)
    const prevMonth = Moment().month(monthNumber).subtract(1, 'month')

    const currMonthStart = currMonth.startOf('month').toDate()
    const prevMonthStart = prevMonth.startOf('month').toDate()
    const prevMonthEnd = prevMonth.endOf('month').toDate()

    const promise = this.loadData(prevMonthStart, prevMonthEnd)
      .then(function (docs) {
        let income = 0.0
        let expense = 0.0
        docs.forEach(function (entry) {
          if (entry.amount >= 0.0) {
            income += entry.amount
          } else {
            expense += entry.amount
          }
        })

        // insert record for first day of monthNumber
        //  - Income, Category: Constants.ROLLOVER_CATEGORY, amount: income + expense
        const savePromise = self.save(
          {
            type: Constants.TYPE_INCOME,
            date: currMonthStart,
            icon: 'mdi-transfer',
            category: Constants.ROLLOVER_CATEGORY,
            amount: income + expense,
            tags: ['Sixpence', 'Balance Rollover']
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
  ensureRollover: function (monthNumber, existsOk = true) {
    const self = this

    const currMonthStart = Moment().month(monthNumber).startOf('month').toDate()
    const currMonthEnd = Moment().month(monthNumber).endOf('month').toDate()

    const promise = this.search(currMonthStart, currMonthEnd, { category: Constants.ROLLOVER_CATEGORY })
      .then(function (docs) {
        let doc = null

        if (docs.length !== 0) {
          doc = docs[0]
        }

        return doc
      })
      .then(function (doc) {
        let action = null

        if (doc) {
          if (!existsOk) {
            action = 'delete+create'
          }
        } else {
          action = 'create'
        }

        return ({ action: action, doc: doc })
      })
      .then(function (result) {
        console.log(result)

        if (result.action === 'create') {
          console.log('Create rollover entry')
          return self._createRolloverEntry(monthNumber)
        } else if (result.action === 'delete+create') {
          console.log('Delete & Create rollover entry')
          self.delete(result.doc._id)
            .then(function (count) {
              console.log(`Deleted ${count} entries.`)
              return self._createRolloverEntry(monthNumber)
            })
            .catch((err) => {
              console.log(err)
            })
        } else {
          console.log('Not creating rollover entry')
          return Promise.resolve(true)
        }
      })
      .catch(function (err) {
        return Promise.reject(err)
      })

    return promise
  },

  count: function (searchTerms) {
    const promise = new Promise(function (resolve, reject) {
      _DB.count(searchTerms)
        .exec(function (err, numDocs) {
          if (err) {
            reject(err)
          } else {
            resolve(numDocs)
          }
        })
    })

    return promise
  },

  delete: function (id) {
    const promise = new Promise(function (resolve, reject) {
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
    const promise = new Promise(function (resolve, reject) {
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
