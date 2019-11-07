import Datastore from 'nedb'
import Moment from 'moment'

const { app } = require('electron').remote
// -----------------------------------------------------------------------------
const dbFileName = (process.env.NODE_ENV === 'development') ? 'budget-dev.sxp' : 'budget.sxp'
var _DB = new Datastore({
  filename: app.getPath('documents') + '/Sixpence/' + dbFileName,
  autoload: true,
  timestampData: true
})
// -----------------------------------------------------------------------------
function computePeriod (freq, firstDue) {
  var due = []
  var willGet = (12 - firstDue) + 1
  var moreNeeded = 12 - willGet

  for (var m = firstDue; m <= 12 + moreNeeded; m += freq) {
    // for (var m = firstDue; m <= 12; m += freq) {
    var dueInMonth = m <= 12 ? m : m - 12
    due.push(dueInMonth)
  }

  return due
}
// -----------------------------------------------------------------------------
function due (month, freq, firstDue) {
  var isDue = false

  var dueMonths = computePeriod(freq, firstDue)
  isDue = dueMonths.includes(month)

  return isDue
}

// Generate a query to find entries that were active between the given dates
var activeBetween = function (start, end) {
  var startDate = Moment(start)
  var endDate = Moment(end)
  return {
    $or: [
      { archivedAt: null },
      {
        $where: function () {
          return this.archivedAt >= startDate.startOf('month') && this.archivedAt <= endDate.endOf('month')
        }
      }
    ]
  }
}

// Generate a query to find entries that were active after the given date
var activeAfter = function (aDate) {
  var afterDate = Moment(aDate)
  return {
    $or: [
      { archivedAt: null },
      {
        $where: function () {
          return this.archivedAt >= afterDate.startOf('month')
        }
      }
    ]
  }
}

// Some very useful, canned queries
const QUERIES = {
  ALL: {},
  ARCHIVED: { archivedAt: { $ne: null } },
  UNARCHIVED: { archivedAt: null },
  ACTIVE: activeBetween(Moment(), Moment()),
  ACTIVE_BETWEEN: activeBetween,
  ACTIVE_AFTER: activeAfter
}
// -----------------------------------------------------------------------------
export default {

  // Canned Queries
  QUERIES: QUERIES,

  compact: function (cb) {
    _DB.persistence.compactDatafile()
    _DB.once('compaction.done', (event) => {
      cb()
    })
  },

  // ---------------------------------------------
  // Load Budget Entries
  // ---------------------------------------------
  // By default load ALL entries
  // -- Params --
  // query: A valid NeDb query. Defaults to: {}
  //        See "canned" queries (above) for some useful options.
  // -- Return --
  // A promise
  getEntries: function (query = QUERIES.ALL) {
    var promise = new Promise(function (resolve, reject) {
      _DB
        .find(query)
        .sort({ type: 1, category: 1, amount: -1 })
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

  // ---------------------------------------------
  // Load Budget Categories
  // ---------------------------------------------
  // By default load ALL categories
  // -- Params --
  // query: A valid NeDb query. Defaults to: {}
  //        See "canned" queries (above) for some useful options.
  // -- Return --
  // A promise
  getCategories: function (query = QUERIES.ALL) {
    var fields = {
      _id: 0,
      icon: 1,
      category: 1
    }

    var promise = new Promise(function (resolve, reject) {
      _DB.find(query, fields).sort({ category: 1 }).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          var uniqueCats = {}
          docs.forEach(function (doc) {
            uniqueCats[doc.category] = doc.icon
          })
          resolve(uniqueCats)
        }
      })
    })

    return promise
  },

  // Load Budget entries for categories that are due in the given `month` based
  // on each entry's frequency and firstDue.
  // Arrange as look-up table by category
  loadCategoryDataByMonth: function (date) {
    var aDate = Moment(date).date(1)
    var month = aDate.month()
    var query = activeAfter(aDate)

    var promise = new Promise(function (resolve, reject) {
      _DB.find(query, { _id: 0, frequency: 1, firstDue: 1, category: 1, amount: 1 })
        .sort({ category: 1 })
        .exec(function (err, docs) {
          if (err) {
            reject(err)
          } else {
            var entries = docs.filter(entry => due(month + 1, entry.frequency, entry.firstDue))
            var catMap = {}

            entries.forEach(function (entry) {
              if (!catMap.hasOwnProperty(entry.category)) {
                catMap[entry.category] = 0.0
              }

              catMap[entry.category] += entry.amount
            })

            resolve(catMap)
          }
        })
    })

    return promise
  },

  categoryType: function (catName) {
    var promise = new Promise(function (resolve, reject) {
      _DB.find({ category: catName }).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          if (docs.length > 0) {
            resolve(docs[0].type)
          } else {
            resolve(null)
          }
        }
      })
    })

    return promise
  },

  count: function (searchTerms) {
    var promise = new Promise(function (resolve, reject) {
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

  search: function (searchTerms, sort = { type: 1, category: 1, amount: -1 }) {
    var promise = new Promise(function (resolve, reject) {
      _DB.find(searchTerms).sort(sort).exec(function (err, docs) {
        if (err) {
          reject(err)
        } else {
          resolve(docs)
        }
      })
    })

    return promise
  },

  bulkUpdate: function (query, updateData) {
    var promise = new Promise(function (resolve, reject) {
      _DB.update(query, updateData, { multi: true }, function (err, numReplaced) {
        if (err) {
          reject(err)
        } else {
          resolve(numReplaced)
        }
      })
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
  },

  isDue: due
}
